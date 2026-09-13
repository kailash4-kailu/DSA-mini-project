"""
Setup Script
Initializes the database, generates data, and trains the ML model.
"""
import os
import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run_step(description, cmd):
    logger.info("Step: %s", description)
    result = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error("FAILED: %s\n%s", description, result.stderr)
        return False
    if result.stdout:
        logger.info(result.stdout.strip())
    return True


def main():
    python = sys.executable

    steps = [
        ("Generate sensor data", [python, "data/generate_data.py", "--records", "5000"]),
        ("Reset database", [python, "scripts/reset_database.py"]),
        ("Train ML model", [python, "ml/train_model.py"]),
    ]

    for desc, cmd in steps:
        if not run_step(desc, cmd):
            logger.error("Setup failed at: %s", desc)
            sys.exit(1)

    logger.info("✅ Setup complete! You can now run the pipeline.")
    logger.info("  1. Start stream processor:  python processor/stream_processor.py")
    logger.info("  2. Start dashboard:         streamlit run dashboard/app.py")
    logger.info("  3. Start producer:           python kafka/producer.py")


if __name__ == "__main__":
    main()
