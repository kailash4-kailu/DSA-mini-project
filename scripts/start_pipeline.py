"""
Start Pipeline Script
Starts the stream processor, dashboard, and producer in separate processes.
"""
import os
import sys
import subprocess
import time
import signal
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
python = sys.executable

processes = []


def cleanup(signum=None, frame=None):
    logger.info("Shutting down pipeline…")
    for name, proc in processes:
        logger.info("Stopping %s (PID %d)", name, proc.pid)
        proc.terminate()
    for name, proc in processes:
        proc.wait(timeout=5)
    logger.info("All processes stopped.")
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    # 1. Stream Processor
    logger.info("Starting Stream Processor…")
    proc_processor = subprocess.Popen(
        [python, "processor/stream_processor.py"],
        cwd=PROJECT_ROOT,
    )
    processes.append(("Stream Processor", proc_processor))
    time.sleep(2)

    # 2. Dashboard
    logger.info("Starting Streamlit Dashboard…")
    proc_dashboard = subprocess.Popen(
        [python, "-m", "streamlit", "run", "dashboard/app.py", "--server.port", "8501"],
        cwd=PROJECT_ROOT,
    )
    processes.append(("Dashboard", proc_dashboard))
    time.sleep(2)

    # 3. Producer
    logger.info("Starting Kafka Producer…")
    proc_producer = subprocess.Popen(
        [python, "kafka/producer.py"],
        cwd=PROJECT_ROOT,
    )
    processes.append(("Producer", proc_producer))

    logger.info("✅ Pipeline running!")
    logger.info("   Dashboard: http://localhost:8501")
    logger.info("   Press Ctrl+C to stop all components.")

    try:
        # Wait for any process to exit
        while True:
            for name, proc in processes:
                ret = proc.poll()
                if ret is not None:
                    logger.warning("%s exited with code %d", name, ret)
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup()


if __name__ == "__main__":
    main()
