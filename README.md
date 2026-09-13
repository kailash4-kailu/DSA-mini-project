# Real-Time IoT Sensor Streaming Analytics and Anomaly Detection System

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Problem Statement](#problem-statement)
3. [Objectives](#objectives)
4. [Features](#features)
5. [Six-Layer Architecture](#six-layer-architecture)
6. [Technology Stack](#technology-stack)
7. [DSA Concepts](#dsa-concepts)
8. [Machine Learning](#machine-learning)
9. [Database Design](#database-design)
10. [Project Structure](#project-structure)
11. [Installation](#installation)
12. [Environment Setup](#environment-setup)
13. [Docker Setup](#docker-setup)
14. [Dataset Generation](#dataset-generation)
15. [Model Training](#model-training)
16. [Running the Pipeline](#running-the-pipeline)
17. [Testing](#testing)
18. [Expected Output](#expected-output)
19. [Troubleshooting](#troubleshooting)
20. [Complexity Analysis](#complexity-analysis)
21. [Future Enhancements](#future-enhancements)

---

## Project Overview

A complete **end-to-end real-time streaming analytics** system that ingests IoT sensor data through Apache Kafka, processes it with DSA data structures and an Isolation Forest ML model, stores results in MySQL, and displays live updates on a professional Streamlit dashboard.

The system demonstrates all six layers of a Data Stream Analytics pipeline:
**Data Source → Streaming → Processing → ML → Database → Visualization**

---

## Problem Statement

Industrial IoT sensors generate massive volumes of continuous data. Detecting anomalies in real-time is critical for preventing equipment failures, safety hazards, and operational disruptions. Traditional batch processing introduces unacceptable latency. This project implements a streaming pipeline that detects anomalies as they happen.

---

## Objectives

1. Build a complete six-layer DSA pipeline
2. Implement real-time data streaming with Apache Kafka
3. Apply DSA data structures (deque, dictionary, heap) for efficient stream processing
4. Use Isolation Forest for real-time anomaly detection
5. Store processed data in MySQL for persistence and querying
6. Create a live-updating Streamlit dashboard for monitoring
7. Demonstrate O(1) and O(log n) streaming algorithms

---

## Features

- **Realistic IoT data generation** with controllable anomaly injection
- **Kafka streaming** with configurable delay for demo-friendly speeds
- **Sliding window processing** using `collections.deque`
- **O(1) running statistics** (count, sum, average, min, max) per device
- **Heap-based top-N anomaly tracking** using `heapq`
- **Isolation Forest ML** for unsupervised anomaly detection
- **MySQL persistence** with per-device metrics aggregation
- **Professional Streamlit dashboard** with auto-refresh, KPI cards, and Plotly charts
- **Docker Compose** infrastructure for Kafka + MySQL

---

## Six-Layer Architecture

```
┌───────────────────────────────────────────────────────────────┐
│  Layer 1: DATA SOURCE                                         │
│  IoT Sensor Data Generator (data/generate_data.py)            │
│  → sensor_data.csv with temperature, humidity, pressure,      │
│    vibration, device_id, timestamp                             │
├───────────────────────────────────────────────────────────────┤
│  Layer 2: STREAMING TOOL                                      │
│  Apache Kafka (kafka/producer.py)                              │
│  → Reads CSV row-by-row, sends JSON to topic                  │
│    "iot-sensor-events" with configurable delay                 │
├───────────────────────────────────────────────────────────────┤
│  Layer 3: STREAM PROCESSOR                                    │
│  Python Consumer (processor/stream_processor.py)               │
│  → Consumes from Kafka, validates, applies DSA structures,    │
│    scores with ML model, writes to MySQL                       │
├───────────────────────────────────────────────────────────────┤
│  Layer 4: ML ALGORITHM                                        │
│  Isolation Forest (ml/train_model.py, ml/model_utils.py)       │
│  → Trained offline, loaded once, scores each event in O(t·logψ)│
├───────────────────────────────────────────────────────────────┤
│  Layer 5: DATABASE                                            │
│  MySQL (database/schema.sql, database/db.py)                   │
│  → sensor_readings table + sensor_metrics aggregation table    │
├───────────────────────────────────────────────────────────────┤
│  Layer 6: VISUALIZATION                                       │
│  Streamlit + Plotly (dashboard/app.py)                         │
│  → Auto-refreshing dashboard with KPIs, charts, anomaly viz   │
└───────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.11+ |
| Streaming | Apache Kafka (Confluent Docker image) |
| Kafka Client | kafka-python-ng |
| Stream Processing | Custom Python processor |
| ML Algorithm | scikit-learn IsolationForest |
| Database | MySQL 8.0 |
| Dashboard | Streamlit + Plotly |
| Model Persistence | joblib |
| Infrastructure | Docker, Docker Compose |
| Data Processing | pandas, numpy |
| Testing | pytest |
| Configuration | python-dotenv |

---

## DSA Concepts

### A. Deque / Sliding Window

**File:** `processor/window_manager.py`

Uses `collections.deque(maxlen=30)` to maintain the last 30 readings per metric per device.

**Why deque?**
- `append()` is **O(1)** – constant time to add new readings
- Auto-eviction of oldest element is **O(1)** via `maxlen` (no manual `pop(0)`)
- A Python list would require **O(n)** for `pop(0)` due to element shifting

```python
from collections import deque
window = deque(maxlen=30)  # Fixed sliding window
window.append(new_value)   # O(1) – oldest auto-evicted when full
avg = sum(window) / len(window)  # Rolling average
```

### B. Hash Map / Dictionary

**Files:** `processor/window_manager.py`, `processor/statistics.py`

Nested dictionaries `{device_id: {metric: data_structure}}` provide:
- **O(1) average** lookup for any device's window or statistics
- Dynamic creation of new device entries on first sight

### C. Heap / Priority Queue

**File:** `processor/anomaly_tracker.py`

Uses `heapq` to maintain the **top N most anomalous** events:
- **O(log N) insertion** – much faster than sorting all events
- **O(1) peek** at the threshold (least anomalous in top-N)
- **O(N) space** – bounded regardless of total events processed

### D. Running Statistics

**File:** `processor/statistics.py`

Maintains streaming count, sum, average, min, max **without re-scanning history**:

```python
# O(1) per update – no O(n) re-scan needed!
count += 1
total += value
avg = total / count
min_val = min(min_val, value)
max_val = max(max_val, value)
```

### E. Time/Window Processing

The sliding window shows how the window state changes as new events arrive:
- Window fills up (first 30 events)
- Window slides (event 31+ evicts oldest)
- Rolling metrics update in O(w) where w is fixed window size

---

## Machine Learning

### Why Isolation Forest?

1. **Unsupervised** – no labeled anomaly data required
2. **Efficient** – O(n·t·log ψ) training, O(t·log ψ) per-sample scoring
3. **Designed for anomaly detection** – isolates outliers, not the norm
4. **Low latency** – suitable for real-time streaming applications

### Training Process (Offline)

```bash
python ml/train_model.py
```

1. Load historical CSV data
2. Extract features: temperature, humidity, pressure, vibration
3. StandardScaler normalization
4. Fit IsolationForest (n_estimators=200, contamination=0.05)
5. Save model + scaler to `models/anomaly_model.pkl`

### Live Scoring (Online)

- Model loaded **once** at processor startup
- Each incoming event: scale features → `decision_function()` → score
- `predict()` returns -1 (anomaly) or 1 (normal)
- Score: lower/more negative = more anomalous

### Contamination Parameter

Set to 0.05 (5%) matching the data generator's anomaly fraction. This tells the model approximately what percentage of training data are outliers.

---

## Database Design

### sensor_readings

Stores every processed event with rolling metrics and anomaly scores.

| Column | Type | Description |
|---|---|---|
| id | BIGINT PK | Auto-increment |
| timestamp | DATETIME(3) | Event timestamp |
| device_id | VARCHAR(32) | Sensor device ID |
| temperature | DOUBLE | Temperature °C |
| humidity | DOUBLE | Humidity % |
| pressure | DOUBLE | Pressure hPa |
| vibration | DOUBLE | Vibration mm/s |
| rolling_temperature | DOUBLE | 30-point rolling avg |
| rolling_humidity | DOUBLE | 30-point rolling avg |
| rolling_pressure | DOUBLE | 30-point rolling avg |
| rolling_vibration | DOUBLE | 30-point rolling avg |
| anomaly_score | DOUBLE | IF decision score |
| is_anomaly | TINYINT(1) | 0=normal, 1=anomaly |
| processed_at | DATETIME(3) | Processing timestamp |

### sensor_metrics

Per-device aggregate metrics, upserted on each event.

---

## Project Structure

```
dsa/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── docker-compose.yml                 # Kafka + MySQL infrastructure
├── .env.example                       # Environment variable template
├── .gitignore
│
├── data/
│   ├── generate_data.py               # Dataset generator
│   └── sensor_data.csv                # Generated dataset
│
├── kafka/
│   ├── __init__.py
│   ├── producer.py                    # Kafka producer (CSV → Kafka)
│   └── consumer_config.py            # Consumer configuration
│
├── processor/
│   ├── __init__.py
│   ├── stream_processor.py            # Main stream processor
│   ├── window_manager.py              # Deque sliding windows
│   ├── statistics.py                  # Running statistics
│   └── anomaly_tracker.py             # Heap top-N tracker
│
├── ml/
│   ├── __init__.py
│   ├── train_model.py                 # Offline model training
│   └── model_utils.py                 # Real-time scoring utility
│
├── models/
│   └── anomaly_model.pkl              # Trained model (generated)
│
├── database/
│   ├── __init__.py
│   ├── schema.sql                     # MySQL schema
│   └── db.py                          # Database helper module
│
├── dashboard/
│   └── app.py                         # Streamlit dashboard
│
├── tests/
│   ├── __init__.py
│   ├── test_window.py                 # Sliding window tests
│   ├── test_statistics.py             # Running statistics tests
│   ├── test_anomaly_tracker.py        # Heap tracker tests
│   └── test_data.py                   # Data generator tests
│
├── docs/
│   ├── architecture.mmd               # Mermaid architecture diagram
│   ├── report.md                      # College report
│   ├── presentation.md                # Slide-by-slide presentation
│   └── demo_script.md                 # Live demo script
│
└── scripts/
    ├── setup.py                       # One-command setup
    ├── start_pipeline.py              # Start all components
    └── reset_database.py              # Database reset
```

---

## Installation

### Prerequisites

- Python 3.11+
- Docker Desktop (for Kafka + MySQL)
- pip

### Step 1: Clone / Navigate to project

```bash
cd path/to/dsa
```

### Step 2: Install Python dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Copy environment file

```bash
copy .env.example .env
# Edit .env if needed (change passwords, ports, etc.)
```

---

## Environment Setup

Edit `.env` to configure:

```env
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC=iot-sensor-events
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=iot_streaming
MYSQL_USER=root
MYSQL_PASSWORD=changeme_secret
STREAM_DELAY=0.5
DASHBOARD_REFRESH_SECONDS=3
MODEL_PATH=models/anomaly_model.pkl
CONTAMINATION=0.05
```

---

## Docker Setup

Start Kafka and MySQL:

```bash
docker compose up -d
```

Verify services are running:

```bash
docker compose ps
```

Wait ~30 seconds for services to fully initialize.

To stop:

```bash
docker compose down
```

To completely reset (remove volumes):

```bash
docker compose down -v
```

---

## Dataset Generation

Generate 5000 sensor records with 5% anomalies:

```bash
python data/generate_data.py --records 5000 --anomaly-fraction 0.05
```

Output: `data/sensor_data.csv`

Options:
- `--records N` – number of records (default: 5000)
- `--anomaly-fraction F` – fraction of anomalies (default: 0.05)
- `--seed S` – random seed (default: 42)
- `--output PATH` – custom output path

---

## Model Training

Train the Isolation Forest on the generated data:

```bash
python ml/train_model.py
```

Output: `models/anomaly_model.pkl`

Options:
- `--data PATH` – training data CSV
- `--model PATH` – output model path
- `--contamination F` – anomaly fraction (default: 0.05)

---

## Running the Pipeline

### Option A: Manual (Recommended for demos)

Open three separate terminals:

**Terminal 1 – Stream Processor:**
```bash
python processor/stream_processor.py
```

**Terminal 2 – Dashboard:**
```bash
streamlit run dashboard/app.py
```

**Terminal 3 – Kafka Producer:**
```bash
python kafka/producer.py --delay 0.5
```

### Option B: All-in-one

```bash
python scripts/start_pipeline.py
```

### Option C: Full setup + run

```bash
python scripts/setup.py           # Generate data, reset DB, train model
python scripts/start_pipeline.py  # Start all components
```

### Dashboard URL

Open: **http://localhost:8501**

---

## Testing

Run all tests:

```bash
pytest tests/ -v
```

### Test Coverage

| Test File | What it tests |
|---|---|
| `test_window.py` | Sliding window, eviction, rolling avg/min/max |
| `test_statistics.py` | Running stats O(1) updates, anomaly counting |
| `test_anomaly_tracker.py` | Heap top-N maintenance, sorting, eviction |
| `test_data.py` | Data generation, ranges, reproducibility |

---

## Expected Output

When the pipeline is running:

1. **Producer** logs: `Sent 50 events to topic 'iot-sensor-events'`
2. **Processor** logs: `Processed 50 events | last device=sensor-03 anomaly=True score=-0.1234`
3. **Dashboard** shows:
   - KPI cards updating in real-time
   - Temperature chart growing with new data points
   - Rolling average smoothing the signal
   - Anomalies marked as red X on the chart
   - Recent events table with newest data
   - Device metrics summary

---

## Troubleshooting

| Problem | Solution |
|---|---|
| Kafka connection refused | Wait 30s after `docker compose up`. Check `docker compose ps`. |
| MySQL connection refused | Ensure MySQL container is running. Check port 3306. |
| `NoBrokersAvailable` | Kafka not ready. Producer has automatic retry logic. |
| Model file not found | Run `python ml/train_model.py` first. |
| Empty dashboard | Start the producer – data flows: Producer → Kafka → Processor → MySQL → Dashboard |
| Dashboard not updating | Ensure processor is running and connected to MySQL. |
| Import errors | Run `pip install -r requirements.txt`. Ensure project root is the working directory. |
| Permission denied on port | Change ports in `.env` and `docker-compose.yml`. |

---

## Complexity Analysis

### DSA Operations

| Operation | Data Structure | Time Complexity | Space Complexity |
|---|---|---|---|
| Add sensor reading to window | `deque` | **O(1)** | O(w) |
| Auto-evict oldest reading | `deque` (maxlen) | **O(1)** | – |
| Calculate rolling average | `deque` | O(w) | O(1) |
| Calculate rolling min/max | `deque` | O(w) | O(1) |
| Lookup device state | `dict` | **O(1)** avg | O(1) |
| Update running statistics | accumulators | **O(1)** | O(1) |
| Add to top-N anomaly heap | `heapq` | **O(log N)** | O(N) |
| Replace root of heap | `heapq` | **O(log N)** | – |
| Peek at heap threshold | `heapq` | **O(1)** | – |
| Get sorted top anomalies | `heapq` | O(N log N) | O(N) |

Where:
- w = window size (30) – constant
- N = max heap size (20) – constant
- d = number of devices

### ML Operations

| Operation | Time Complexity |
|---|---|
| Train IsolationForest | O(n · t · log ψ) |
| Score single event | O(t · log ψ) |

Where t = number of trees (200), ψ = subsample size

### Per-Event Processing

Total per-event cost: **O(1)** amortized (all DSA operations are O(1) or O(log N) with fixed N).

---

## Future Enhancements

1. **Apache Flink/Spark Structured Streaming** for distributed processing
2. **Multiple anomaly algorithms** (SVM, K-Means clustering)
3. **Alerting system** (email/SMS on critical anomalies)
4. **Historical analysis** dashboards with date range filtering
5. **Multi-sensor correlation** analysis
6. **Grafana** integration for production monitoring
7. **Model retraining pipeline** with new data
8. **Kubernetes** deployment for scalability
9. **Time-series database** (InfluxDB/TimescaleDB) for better performance
10. **Edge computing** integration for pre-processing at sensor level
