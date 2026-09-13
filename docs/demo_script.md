# Live Demo Script
## Real-Time IoT Sensor Streaming Analytics and Anomaly Detection System

**Estimated Time: 8–10 minutes**

---

## Pre-Demo Checklist

Before starting the demo, ensure:
- [ ] Docker Desktop is running
- [ ] Python dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file exists (copy from `.env.example`)
- [ ] No other services on ports 9092, 3306, 8501

---

## Step 1: Start Infrastructure (1 minute)

**Open a terminal in the project root.**

```bash
docker compose up -d
```

**Say:**
> "We're starting Apache Kafka and MySQL using Docker Compose. Kafka is our message broker for streaming, and MySQL is our serving database."

**Wait 30 seconds for services to initialize.**

Verify:
```bash
docker compose ps
```

All services should show "running".

---

## Step 2: Generate Dataset (30 seconds)

```bash
python data/generate_data.py --records 5000 --anomaly-fraction 0.05
```

**Say:**
> "We've generated 5000 simulated IoT sensor readings with 5% anomalies injected. This includes temperature, humidity, pressure, and vibration data from 5 virtual sensors. The anomalies simulate real-world failures like temperature spikes and pressure drops."

---

## Step 3: Train the ML Model (30 seconds)

```bash
python ml/train_model.py
```

**Say:**
> "We're training an Isolation Forest model offline on the historical data. This is important — we train once and then load the model for real-time scoring. We don't retrain for every event. The model detected 250 anomalies in training, exactly 5%."

---

## Step 4: Reset Database (15 seconds)

```bash
python scripts/reset_database.py
```

**Say:**
> "We're initializing a clean MySQL database with our schema — a sensor_readings table for all processed events and a sensor_metrics table for per-device aggregates."

---

## Step 5: Start the Stream Processor (30 seconds)

**Open Terminal 2:**

```bash
python processor/stream_processor.py
```

**Say:**
> "The stream processor is now listening on the Kafka topic 'iot-sensor-events'. When events arrive, it will: validate the data, update sliding windows using a deque data structure, calculate running statistics in O(1), score with the Isolation Forest model, update the heap-based anomaly tracker, and write everything to MySQL."

---

## Step 6: Start the Dashboard (30 seconds)

**Open Terminal 3:**

```bash
streamlit run dashboard/app.py
```

**Open browser to http://localhost:8501**

**Say:**
> "This is our Streamlit dashboard. Right now it shows 'Waiting for data' because we haven't started the producer yet. The dashboard auto-refreshes every 3 seconds by querying MySQL."

---

## Step 7: Start the Producer — THE KEY MOMENT (1 minute)

**Open Terminal 4:**

```bash
python kafka/producer.py --delay 0.5
```

**Say:**
> "Now watch the dashboard! The producer is reading sensor data one record at a time and sending it to Kafka with a 0.5-second delay. This simulates real-time IoT sensor data arrival."

**Point to the dashboard:**
> "You can see the KPI cards updating — temperature, humidity, pressure, vibration readings changing in real-time. The total readings counter is incrementing."

---

## Step 8: Show Live Charts (1 minute)

**Point to the Temperature chart:**
> "This live chart shows temperature readings as they arrive. Each point is a real event that traveled through Kafka → Processor → MySQL → Dashboard."

**Point to the Rolling Average chart:**
> "Here you can see the actual temperature vs. the 30-point rolling average. The rolling average is calculated using a deque-based sliding window — this is our key DSA data structure. The deque allows O(1) append and O(1) eviction of old data."

---

## Step 9: Show Anomaly Detection (1 minute)

**Point to the Anomaly chart:**
> "Green dots are normal readings. Red X marks are anomalies detected by the Isolation Forest in real-time. Notice how anomalies often correspond to temperature spikes — these are the injected anomalies our model correctly identifies."

**Point to the KPI cards:**
> "The anomaly counter increases as anomalies are detected. The sensor status shows NORMAL, WARNING, or CRITICAL based on the recent anomaly ratio."

---

## Step 10: Show Device Filter (30 seconds)

**Use the sidebar device filter to select 'sensor-01':**
> "We can filter by device. Each device maintains its own sliding window, running statistics, and anomaly tracking — all using dictionary-based lookups for O(1) access."

---

## Step 11: Show Top Anomalies Table (30 seconds)

**Scroll to Top Anomalies:**
> "This table shows the most anomalous events ranked by score. We maintain this using a heap-based priority queue — heapq in Python. Insertion is O(log N) and we only keep the top 20, so memory is bounded regardless of how many events we process."

---

## Step 12: Pause the Producer (30 seconds)

**Press Ctrl+C in the producer terminal.**

**Say:**
> "I've stopped the producer. Watch the dashboard — it will freeze because no new data is flowing through the pipeline. This proves the dashboard is showing REAL streaming data, not a fake animation."

**Wait 10 seconds for the dashboard to show no changes.**

---

## Step 13: Resume the Producer (30 seconds)

**Restart the producer:**
```bash
python kafka/producer.py --delay 0.5
```

**Say:**
> "Producer restarted. Watch the dashboard resume updating — data is flowing again through the complete pipeline: CSV → Kafka → Processor → ML scoring → MySQL → Dashboard."

---

## Step 14: Conclude (1 minute)

**Say:**
> "To summarize, this project demonstrates all six layers of a Data Stream Analytics pipeline:
> 1. **Data Source** — IoT sensor data generator
> 2. **Streaming** — Apache Kafka
> 3. **Stream Processing** — Python with DSA data structures
> 4. **ML** — Isolation Forest for anomaly detection
> 5. **Database** — MySQL for persistence
> 6. **Visualization** — Streamlit with Plotly
>
> Key DSA concepts:
> - **Deque/sliding window** — O(1) append and eviction
> - **Dictionary/hash map** — O(1) device state lookup
> - **Heap/priority queue** — O(log N) top-anomaly tracking
> - **Running statistics** — O(1) count/sum/avg/min/max updates
>
> All operations on each incoming event are O(1) or O(log N) — the system can scale to millions of events."

---

## Cleanup

After the demo:
```bash
# Stop all Python processes (Ctrl+C in each terminal)
# Stop Docker services
docker compose down
```

To fully reset:
```bash
docker compose down -v  # removes all data
```
