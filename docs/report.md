# Real-Time IoT Sensor Streaming Analytics and Anomaly Detection System

## College Report — Data Stream Analytics (DSA) Mini Project

---

## 1. Title & Metadata

**Real-Time IoT Sensor Streaming Analytics and Anomaly Detection System**

A comprehensive Data Stream Analytics project demonstrating real-time IoT sensor monitoring with streaming technology, DSA data structures, machine learning, and live dashboard visualization.

**Course / Subject:** Data Stream Analytics (DSA Mini Project)  
**Group No:** 3  
**Group Members:**
- 23BTRCL227 — P CHETHAN
- 23BTRCL217 — MUKKAMALLA LOKESHWAR REDDY
- 23BTRCL221 — NADAKUDURU SRINIVAS
- 23BTRCL233 — SOMISETTY JAGANNADA KAILASH

**Submitted To:** Dr. Archana Sasi (Course Coordinator / Faculty, Data Stream Analytics)

---

## 2. Abstract

This project implements a complete end-to-end real-time streaming analytics pipeline for IoT sensor data. The system simulates continuous sensor readings (temperature, humidity, pressure, vibration) from multiple industrial IoT devices, streams them through Apache Kafka, processes each event using efficient DSA data structures (deque-based sliding windows, hash maps, and heap-based priority queues), detects anomalies in real-time using an Isolation Forest machine learning model, persists results in MySQL, and visualizes live data on a professional Streamlit dashboard. The system demonstrates all six layers of a Data Stream Analytics architecture and processes each incoming event in O(1) amortized time.

---

## 3. Introduction

The Internet of Things (IoT) has transformed industrial operations by enabling continuous monitoring of equipment and environmental conditions through networked sensors. Modern industrial facilities deploy thousands of sensors that generate millions of data points per day, measuring parameters such as temperature, humidity, pressure, and vibration.

Traditional batch processing approaches, which collect data and analyze it periodically, are inadequate for time-critical applications. Equipment failures, safety hazards, and quality issues require immediate detection and response. This necessitates stream processing — analyzing data as it arrives, event by event.

Data Stream Analytics (DSA) provides the theoretical foundation and practical tools for processing unbounded, continuous data streams efficiently. Key challenges include:
- Processing each event with bounded latency
- Maintaining state without storing the entire history
- Detecting patterns and anomalies in real-time
- Scaling to handle high-throughput data streams

This project addresses these challenges by implementing a complete six-layer DSA pipeline using modern technologies and efficient data structures.

---

## 4. Problem Statement

Industrial IoT sensors produce continuous, high-volume data streams that must be monitored for anomalies in real-time. Key challenges include:

1. **Volume**: Thousands of sensors generating readings every second
2. **Velocity**: Data arrives continuously and must be processed with low latency
3. **Variety**: Multiple sensor types with different normal operating ranges
4. **Anomaly Detection**: Identifying abnormal patterns that may indicate equipment failure
5. **Visualization**: Presenting real-time insights to operators for decision-making

The problem requires a system that can:
- Ingest data from multiple sensors continuously
- Process each event efficiently without re-scanning history
- Apply machine learning for automated anomaly detection
- Maintain bounded memory usage regardless of total events processed
- Provide live, auto-updating visualization

---

## 5. Objectives

1. Design and implement a complete six-layer DSA pipeline
2. Simulate realistic IoT sensor data with controllable anomaly injection
3. Implement Apache Kafka for reliable, real-time data streaming
4. Apply DSA data structures (deque, dictionary, heap) for efficient stream processing
5. Train and deploy an Isolation Forest model for real-time anomaly detection
6. Store processed data in MySQL with per-device metric aggregation
7. Create a professional, auto-refreshing Streamlit dashboard
8. Demonstrate O(1) and O(log N) per-event processing complexity
9. Write comprehensive tests for all DSA components

---

## 6. Existing System

Traditional IoT monitoring systems typically use:

- **Batch Processing**: Collect data over time periods, then analyze. This introduces latency of minutes to hours, making real-time anomaly detection impossible.
- **Threshold-Based Alerting**: Simple static thresholds (e.g., "alert if temperature > 50°C"). This misses subtle, multi-dimensional anomalies and produces many false positives.
- **Manual Monitoring**: Human operators watching dashboards. This is expensive, error-prone, and doesn't scale.

**Limitations of existing approaches:**
- High latency in batch systems
- Poor anomaly detection with simple thresholds
- No consideration of multiple sensor dimensions
- No efficient data structure usage for streaming
- Limited scalability

---

## 7. Proposed System

Our system addresses the limitations of existing approaches by implementing:

1. **Real-time streaming** with Apache Kafka for sub-second event delivery
2. **Efficient DSA data structures** for bounded-memory, constant-time processing
3. **Machine learning** (Isolation Forest) for multi-dimensional anomaly detection
4. **Automated pipeline** that processes each event through all six layers
5. **Live dashboard** that auto-refreshes with actual streaming data

**Key differentiators:**
- Events are processed individually as they arrive (not batched)
- Sliding windows use deque for O(1) operations (not lists with O(n))
- Running statistics use accumulators for O(1) updates (not full re-scans)
- Top-N anomaly tracking uses heaps for O(log N) operations (not sorting)
- The entire per-event processing cost is O(1) amortized

---

## 8. System Architecture

The system follows a six-layer architecture:

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 1: DATA SOURCE                                            │
│  IoT Sensor Data Generator → sensor_data.csv                     │
├─────────────────────────────────────────────────────────────────┤
│  Layer 2: STREAMING TOOL                                         │
│  Apache Kafka (Producer → Topic → Consumer)                      │
├─────────────────────────────────────────────────────────────────┤
│  Layer 3: STREAM PROCESSOR                                       │
│  Python Consumer + DSA Data Structures                           │
│  (Sliding Window, Running Stats, Heap, Dictionary)               │
├─────────────────────────────────────────────────────────────────┤
│  Layer 4: ML ALGORITHM                                           │
│  Isolation Forest (trained offline, scored in real-time)          │
├─────────────────────────────────────────────────────────────────┤
│  Layer 5: DATABASE                                               │
│  MySQL (sensor_readings + sensor_metrics tables)                 │
├─────────────────────────────────────────────────────────────────┤
│  Layer 6: VISUALIZATION                                          │
│  Streamlit Dashboard + Plotly Charts (auto-refresh)              │
└─────────────────────────────────────────────────────────────────┘
```

**Data Flow:**
```
CSV File → Kafka Producer → Kafka Topic → Stream Processor
                                              ↓
                               Isolation Forest + DSA Structures
                                              ↓
                                            MySQL
                                              ↓
                                      Streamlit Dashboard
```

---

## 9. Dataset

### Description

The dataset is generated programmatically to simulate realistic IoT sensor behavior:

| Feature | Normal Range | Anomaly Range | Unit |
|---|---|---|---|
| Temperature | 20 – 35 | 50 – 80 (spike) | °C |
| Humidity | 40 – 80 | 5 – 20 (drop) | % |
| Pressure | 1000 – 1025 | 950 – 980 (drop) | hPa |
| Vibration | 0.1 – 1.5 | 5 – 15 (spike) | mm/s |

### Statistics

- Total records: 5000
- Number of devices: 5 (sensor-01 to sensor-05)
- Anomaly fraction: 5% (~250 anomalous records)
- Anomaly types: temperature spike, humidity drop, pressure drop, vibration spike, combinations
- Timestamp precision: milliseconds
- Reproducible with random seed (42)

### Generation

```bash
python data/generate_data.py --records 5000 --anomaly-fraction 0.05 --seed 42
```

---

## 10. Six-Layer Architecture — Detailed

### Layer 1: Data Source

**Component:** `data/generate_data.py`

- Generates realistic IoT sensor data using NumPy random distributions
- Produces CSV files with timestamp, device_id, and four sensor metrics
- Configurable number of records, anomaly fraction, and random seed
- Anomalies are injected by shifting values outside normal operating ranges

### Layer 2: Kafka Streaming

**Component:** `kafka/producer.py`

- Apache Kafka serves as the distributed message broker
- Producer reads CSV row by row (NOT bulk loading)
- Each row is serialized as JSON and sent to the `iot-sensor-events` topic
- Configurable delay between messages (default: 0.5 seconds)
- Automatic retry logic for broker unavailability

### Layer 3: Stream Processing

**Component:** `processor/stream_processor.py`

- Kafka consumer receives events one at a time
- Each event goes through a processing pipeline:
  1. JSON validation and field checking
  2. Sliding window update (deque) → rolling metrics
  3. Running statistics update (accumulators) → count/sum/avg/min/max
  4. ML scoring (Isolation Forest) → anomaly score and flag
  5. Top-N anomaly heap update → tracks most anomalous events
  6. MySQL insertion → sensor_readings
  7. MySQL upsert → sensor_metrics

### Layer 4: Machine Learning

**Component:** `ml/train_model.py`, `ml/model_utils.py`

- Isolation Forest algorithm (scikit-learn)
- Trained offline on historical data
- Model + StandardScaler saved with joblib
- Loaded once at processor startup
- Scores each event in O(t · log ψ) time

### Layer 5: Database

**Component:** `database/schema.sql`, `database/db.py`

- MySQL 8.0 with two main tables
- `sensor_readings`: stores every processed event
- `sensor_metrics`: per-device aggregated metrics (upserted)
- Connection pooling for efficient concurrent access
- Indexed for fast dashboard queries

### Layer 6: Visualization

**Component:** `dashboard/app.py`

- Streamlit with Plotly for professional charts
- Auto-refreshes every 3 seconds
- Reads directly from MySQL (genuine streaming, not fake)
- KPI cards, line charts, anomaly scatter plot, data tables
- Device filter and configurable refresh rate

---

## 11. Data Source — Implementation Details

The data generator uses NumPy's random number generator for reproducible output:

```python
rng = np.random.default_rng(seed=42)
reading = {
    "temperature": rng.uniform(20.0, 35.0),
    "humidity": rng.uniform(40.0, 80.0),
    "pressure": rng.uniform(1000.0, 1025.0),
    "vibration": rng.uniform(0.1, 1.5),
}
```

Anomaly injection modifies one or more values to extreme ranges, simulating real-world sensor failures.

---

## 12. Kafka Streaming — Implementation Details

The Kafka producer sends events one at a time:

```python
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)
for row in csv_reader:
    producer.send("iot-sensor-events", value=row)
    time.sleep(0.5)  # Configurable delay
```

This ensures genuine streaming behavior — events arrive gradually, not all at once.

---

## 13. Stream Processing — Implementation Details

The processor consumes from Kafka and applies all DSA structures:

```python
for message in consumer:
    event = message.value
    # 1. Validate
    if not validate_event(event): continue
    # 2. Sliding window (deque)
    rolling = window_mgr.add_reading(device_id, reading)
    # 3. ML scoring
    score, is_anomaly = scorer.score(reading)
    # 4. Running statistics (O(1))
    stats_tracker.update(device_id, reading, is_anomaly)
    # 5. Heap tracker (O(log N))
    if is_anomaly:
        anomaly_tracker.add(score, reading)
    # 6-7. Database writes
    insert_reading(db_row)
    upsert_metrics(metrics_row)
```

---

## 14. DSA Algorithms and Data Structures

### A. Deque / Sliding Window

**Purpose:** Maintain the last 30 readings per metric per device for rolling statistics.

**Implementation:** `collections.deque(maxlen=30)`

**Why deque over list?**
- `deque.append()`: O(1) — constant time addition
- `deque` with `maxlen` auto-evicts oldest element: O(1)
- `list.pop(0)`: O(n) — requires shifting all elements

```python
from collections import deque
window = deque(maxlen=30)
window.append(new_value)  # O(1), oldest auto-removed when full
```

### B. Hash Map / Dictionary

**Purpose:** Map device IDs to their windows, statistics, and state.

**Implementation:** `dict[str, dict[str, SlidingWindow]]`

**Complexity:** O(1) average for lookup, insertion, and update.

```python
windows = {}  # {device_id: {metric: SlidingWindow}}
windows[device_id][metric].add(value)  # O(1) lookup + O(1) add
```

### C. Heap / Priority Queue

**Purpose:** Track the top N most anomalous sensor events.

**Implementation:** `heapq` (min-heap with negated scores → effective max-heap)

**Complexity:**
- `heappush()`: O(log N)
- `heapreplace()`: O(log N)
- `heap[0]` peek: O(1)
- Space: O(N)

```python
import heapq
if len(heap) < max_size:
    heapq.heappush(heap, (neg_score, seq, reading))
elif neg_score > heap[0][0]:
    heapq.heapreplace(heap, (neg_score, seq, reading))
```

### D. Running Statistics

**Purpose:** Maintain count, sum, average, min, max per metric without re-scanning history.

**Implementation:** Four accumulators per metric.

**Complexity:** O(1) update per new value.

```python
count += 1
total += value
avg = total / count
min_val = min(min_val, value)
max_val = max(max_val, value)
```

---

## 15. Machine Learning Model

### Isolation Forest Algorithm

**Principle:** Anomalies are "few and different." In a random tree, anomalous points require fewer random splits to isolate, resulting in shorter path lengths.

**Training:**
- Algorithm: `sklearn.ensemble.IsolationForest`
- Parameters: `n_estimators=200`, `contamination=0.05`
- Features: temperature, humidity, pressure, vibration
- Pre-processing: StandardScaler normalization
- Training complexity: O(n · t · log ψ)

**Scoring:**
- `decision_function()`: returns a continuous anomaly score
- Lower scores (more negative) indicate more anomalous points
- `predict()`: returns -1 (anomaly) or 1 (normal)
- Scoring complexity: O(t · log ψ) per event

**Why Isolation Forest?**
1. Unsupervised — no labeled anomaly data required
2. Efficient for high-dimensional data
3. Fast scoring suitable for real-time applications
4. Handles multi-dimensional anomalies (not just single-threshold)

---

## 16. Database

### MySQL Schema

**Table: `sensor_readings`**
- Primary table storing every processed event
- Includes raw values, rolling averages, anomaly scores
- Indexed on device_id, timestamp, and is_anomaly for fast queries

**Table: `sensor_metrics`**
- Per-device aggregate metrics (upserted on each event)
- Includes latest values, averages, min/max, anomaly counts
- Provides fast summary queries without full table scans

### Connection Management
- Connection pooling with 5 connections
- Automatic reconnection on failure
- Environment variable-based configuration

---

## 17. Dashboard

The Streamlit dashboard provides:

1. **KPI Cards** — Current sensor values, total readings, anomaly count
2. **Live Temperature Chart** — Real-time temperature readings
3. **Rolling Average Plot** — Actual vs. 30-point rolling average
4. **Anomaly Scatter Plot** — Normal (green) vs. anomaly (red) markers
5. **Multi-Metric Charts** — Humidity and vibration with rolling averages
6. **Device Metrics Table** — Per-device aggregate statistics
7. **Top Anomalies Table** — Highest anomaly-score events
8. **Recent Events Table** — Latest 20 sensor readings
9. **Sensor Status** — NORMAL / WARNING / CRITICAL based on recent anomaly ratio
10. **Device Filter** — Sidebar filter for individual device monitoring

---

## 18. Implementation

### Technology Stack

| Component | Technology | Version |
|---|---|---|
| Programming Language | Python | 3.11+ |
| Streaming | Apache Kafka | 7.6.1 (Confluent) |
| Kafka Client | kafka-python-ng | 2.2.3 |
| ML Framework | scikit-learn | 1.5.1 |
| Database | MySQL | 8.0 |
| Dashboard | Streamlit | 1.37.0 |
| Charting | Plotly | 5.23.0 |
| Data Processing | pandas, numpy | 2.2.2, 1.26.4 |
| Infrastructure | Docker Compose | 3.8 |
| Testing | pytest | 8.3.2 |

### Project Files

| File | Purpose |
|---|---|
| `data/generate_data.py` | IoT dataset generator |
| `kafka/producer.py` | Kafka producer |
| `processor/stream_processor.py` | Main stream processor |
| `processor/window_manager.py` | Deque sliding windows |
| `processor/statistics.py` | Running statistics |
| `processor/anomaly_tracker.py` | Heap anomaly tracker |
| `ml/train_model.py` | Offline model training |
| `ml/model_utils.py` | Real-time scoring |
| `database/schema.sql` | MySQL schema |
| `database/db.py` | Database utilities |
| `dashboard/app.py` | Streamlit dashboard |

---

## 19. Results

### Test Results

All 30 unit tests pass:

| Test Suite | Tests | Result |
|---|---|---|
| Sliding Window (test_window.py) | 9 | ✅ All Pass |
| Running Statistics (test_statistics.py) | 8 | ✅ All Pass |
| Anomaly Tracker (test_anomaly_tracker.py) | 6 | ✅ All Pass |
| Data Generator (test_data.py) | 7 | ✅ All Pass |
| **Total** | **30** | **✅ All Pass** |

### Model Performance

- Training samples: 5000
- Detected anomalies: 250 (5.00%)
- Matches injection rate: ✅

### System Performance

- Per-event processing: O(1) amortized
- Dashboard refresh: every 3 seconds
- End-to-end latency: < 2 seconds (event → visible on dashboard)

---

## 20. Complexity Analysis

### Per-Event Processing Complexity

| Operation | Data Structure | Time | Space |
|---|---|---|---|
| Kafka consume | KafkaConsumer | O(1) | O(1) |
| Event validation | dict lookup | O(1) | O(1) |
| Sliding window update | deque | O(1) | O(w) |
| Rolling average | deque sum | O(w) | O(1) |
| Running stats update | accumulators | O(1) | O(1) |
| ML scoring | IsolationForest | O(t·log ψ) | O(1) |
| Heap update | heapq | O(log N) | O(N) |
| DB insert | MySQL | O(1)* | O(1) |
| **Total per event** | | **O(1)** | **O(w+N)** |

*w=30 (constant), N=20 (constant), t=200 (constant), ψ=256 (constant)
*Since all parameters are constants, the total per-event cost is effectively O(1).

### Space Complexity

| Component | Space |
|---|---|
| Sliding windows | O(d × m × w) = O(5 × 4 × 30) = O(600) |
| Running statistics | O(d × m) = O(20) |
| Anomaly heap | O(N) = O(20) |
| Device state dicts | O(d) = O(5) |
| **Total** | **O(d × m × w)** — bounded |

---

## 21. Advantages

1. **Real-time processing** — sub-second latency from event arrival to dashboard update
2. **Efficient memory usage** — bounded by window size and heap size, not total events
3. **Scalable architecture** — Kafka enables horizontal scaling of producers/consumers
4. **Multi-dimensional anomaly detection** — Isolation Forest considers all sensor dimensions
5. **Professional visualization** — live dashboard suitable for operational monitoring
6. **Modular design** — each component can be independently upgraded or replaced
7. **Reproducible** — deterministic data generation and model training
8. **Containerized infrastructure** — Docker Compose for easy deployment

---

## 22. Limitations

1. **Single-node processing** — not distributed across multiple machines
2. **Offline model training** — model doesn't adapt to concept drift
3. **Simulated data** — uses generated data rather than real IoT sensors
4. **Single Kafka partition** — limits throughput scalability
5. **MySQL for time-series** — a dedicated time-series database would perform better
6. **No alerting** — detects anomalies but doesn't send notifications
7. **Rolling statistics** — linear scan for min/max in window (could use segment tree for O(log w))

---

## 23. Future Scope

1. **Distributed Processing**: Replace Python consumer with Apache Flink or Spark Structured Streaming
2. **Multiple ML Models**: Ensemble approach combining Isolation Forest, SVM, and K-Means
3. **Alerting System**: Email/SMS/Slack notifications on critical anomalies
4. **Online Learning**: Incremental model updates as new data arrives
5. **Edge Computing**: Pre-processing at sensor level to reduce bandwidth
6. **Time-Series Database**: InfluxDB or TimescaleDB for optimized time-series queries
7. **Grafana Integration**: Industry-standard monitoring dashboard
8. **Kubernetes Deployment**: Container orchestration for production scalability
9. **Historical Analysis**: Date range queries and trend analysis
10. **Multi-Sensor Correlation**: Cross-device anomaly detection

---

## 24. Conclusion

This project successfully demonstrates a complete six-layer Data Stream Analytics pipeline for real-time IoT sensor monitoring and anomaly detection. The system:

- Generates realistic IoT sensor data with controlled anomaly injection
- Streams data through Apache Kafka for genuine real-time processing
- Applies DSA data structures (deque, dictionary, heap) for efficient O(1) per-event processing
- Uses Isolation Forest machine learning for multi-dimensional anomaly detection
- Persists processed data in MySQL for serving and querying
- Visualizes live results on a professional Streamlit dashboard with auto-refresh

The project demonstrates that efficient data structures are critical for streaming systems — using a deque instead of a list, accumulators instead of re-scans, and heaps instead of sorting enables constant-time processing regardless of the total number of events.

---

## 25. References

1. Liu, F.T., Ting, K.M. and Zhou, Z.H., 2008. Isolation Forest. In *2008 Eighth IEEE International Conference on Data Mining* (pp. 413-422). IEEE.
2. Apache Kafka Documentation — https://kafka.apache.org/documentation/
3. scikit-learn IsolationForest — https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html
4. Streamlit Documentation — https://docs.streamlit.io/
5. Python collections.deque — https://docs.python.org/3/library/collections.html#collections.deque
6. Python heapq — https://docs.python.org/3/library/heapq.html
7. Cormen, T.H., Leiserson, C.E., Rivest, R.L. and Stein, C., 2009. *Introduction to Algorithms*. MIT Press.
8. MySQL 8.0 Reference Manual — https://dev.mysql.com/doc/refman/8.0/en/
9. Plotly Python Graphing Library — https://plotly.com/python/
10. Docker Compose Documentation — https://docs.docker.com/compose/
