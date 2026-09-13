# Slide-by-Slide Presentation
## Real-Time IoT Sensor Streaming Analytics and Anomaly Detection System

---

## Slide 1: Title Slide

**Title:** Real-Time IoT Sensor Streaming Analytics and Anomaly Detection System

**Subtitle:** A Data Stream Analytics (DSA) Mini Project

**Group No:** 3

**Group Members:**
- 23BTRCL227 — P CHETHAN
- 23BTRCL217 — MUKKAMALLA LOKESHWAR REDDY
- 23BTRCL221 — NADAKUDURU SRINIVAS
- 23BTRCL233 — SOMISETTY JAGANNADA KAILASH

**Submitted To:**
Dr. Archana Sasi (Course Coordinator / Faculty, Data Stream Analytics)

**What to say:**
> "Good morning/afternoon. Today our team will present our DSA mini project: a Real-Time IoT Sensor Streaming Analytics and Anomaly Detection System built using Apache Kafka, core DSA data structures, Isolation Forest, MySQL, and Streamlit."

---

## Slide 2: Problem Statement

**Title:** Problem Statement

**Bullet Points:**
- Industrial IoT sensors generate continuous, high-volume data streams
- Equipment failures and safety hazards must be detected in real-time
- Traditional batch processing introduces unacceptable delays
- Need for automated anomaly detection that works as data arrives
- Manual monitoring of thousands of sensors is impractical

**What to say:**
> "In industrial settings, sensors continuously produce data. If a temperature spikes or vibration increases abnormally, we need to detect it immediately — not hours later in a batch report. This project solves that by building a complete streaming pipeline."

---

## Slide 3: Motivation

**Title:** Why Real-Time Streaming?

**Bullet Points:**
- Batch processing: minutes to hours of latency
- Stream processing: milliseconds to seconds of latency
- Early anomaly detection prevents:
  - Equipment damage
  - Safety incidents
  - Production downtime
  - Costly repairs
- DSA data structures enable efficient per-event processing

**What to say:**
> "The motivation is clear — in streaming, we process each event as it arrives. Using DSA data structures like deques and heaps, we can do this in O(1) or O(log N) time per event, making the system scalable to millions of events."

---

## Slide 4: Objectives

**Title:** Project Objectives

**Bullet Points:**
1. Build a complete six-layer DSA pipeline
2. Implement Apache Kafka for real-time data streaming
3. Apply DSA data structures: deque, dictionary, heap
4. Use Isolation Forest ML for anomaly detection
5. Store and serve processed data from MySQL
6. Create a live-updating monitoring dashboard
7. Demonstrate O(1) and O(log N) streaming algorithms

**What to say:**
> "Our objectives cover all six layers of a DSA system, from data ingestion to visualization, with a strong emphasis on efficient data structures."

---

## Slide 5: System Architecture

**Title:** System Architecture — Six Layers

**Content:** Architecture diagram showing:
```
Data Generator → Kafka Producer → Kafka Topic → Stream Processor
                                                    ↓
                                     Isolation Forest + DSA Structures
                                                    ↓
                                                  MySQL
                                                    ↓
                                            Streamlit Dashboard
```

**What to say:**
> "Here's our complete architecture. Data flows from left to right: generated sensor data enters Kafka, is consumed by our stream processor which applies DSA structures and ML scoring, results go to MySQL, and the dashboard reads from MySQL with auto-refresh."

---

## Slide 6: Data Source (Layer 1)

**Title:** Layer 1: Data Source — IoT Sensor Simulation

**Bullet Points:**
- Simulates 5 IoT sensors (sensor-01 to sensor-05)
- Generates 5000+ sensor readings
- Features: temperature, humidity, pressure, vibration
- Normal operating ranges with 5% anomaly injection
- Anomaly types: temperature spikes, humidity drops, pressure drops, vibration spikes
- Reproducible with configurable random seed

**What to say:**
> "We generate realistic IoT data with controllable anomaly injection. Normal temperature ranges from 20-35°C, but anomalies spike to 50-80°C. This gives us labeled ground truth to verify our detection."

---

## Slide 7: Kafka Streaming (Layer 2)

**Title:** Layer 2: Apache Kafka — Real-Time Streaming

**Bullet Points:**
- Apache Kafka as distributed message broker
- Topic: `iot-sensor-events`
- Producer reads CSV row-by-row (NOT bulk load)
- Configurable delay (0.5s default) for demo visibility
- JSON serialization for each event
- Automatic retry on broker unavailability
- Guarantees ordering within partition

**What to say:**
> "Kafka is our streaming backbone. The producer sends one event at a time with a configurable delay, simulating real-time sensor data. This is genuine streaming — not a fake animation."

---

## Slide 8: Stream Processing (Layer 3)

**Title:** Layer 3: Stream Processor — Event-by-Event Processing

**Bullet Points:**
- Consumes events from Kafka in real-time
- Per-event pipeline:
  1. Validate JSON and required fields
  2. Update sliding windows (deque)
  3. Update running statistics (O(1))
  4. Score with Isolation Forest
  5. Update top-N anomaly heap
  6. Insert into MySQL
  7. Upsert device metrics

**What to say:**
> "Our stream processor handles each event in constant time. It validates, enriches with rolling metrics, scores for anomalies, and persists — all without re-scanning history."

---

## Slide 9: DSA Concepts — Deque & Sliding Window

**Title:** DSA: Deque-based Sliding Window

**Bullet Points:**
- `collections.deque(maxlen=30)` — fixed-size window
- **append()**: O(1) — add new reading
- **auto-eviction**: O(1) — oldest element removed automatically
- Calculates rolling average, min, max per metric per device
- Why not a list? `list.pop(0)` is O(n) — deque is O(1)
- Per-device × per-metric windows using nested dictionaries

**Code Example:**
```python
window = deque(maxlen=30)
window.append(new_reading)  # O(1), auto-evicts oldest
rolling_avg = sum(window) / len(window)
```

**What to say:**
> "The deque is perfect for sliding windows. Unlike a list where removing from the front costs O(n), deque gives us O(1) for both ends. With maxlen, eviction is automatic."

---

## Slide 10: DSA Concepts — Dictionary & Heap

**Title:** DSA: Hash Map & Priority Queue

**Hash Map (dict):**
- `{device_id: {metric: SlidingWindow}}` — O(1) average lookup
- Tracks device state, latest readings, statistics
- Space: O(d × m × w) — devices × metrics × window size

**Heap (heapq):**
- Maintains top-N most anomalous events
- Min-heap with negated scores → effective max-heap
- Insert: O(log N), Peek: O(1), Space: O(N)
- N = 20 (constant) — bounded memory

**What to say:**
> "Dictionaries give us O(1) device lookups. The heap efficiently tracks the top 20 most anomalous events — much better than sorting the entire stream, which would be O(n log n)."

---

## Slide 11: Isolation Forest (Layer 4)

**Title:** Layer 4: Isolation Forest — Anomaly Detection

**Bullet Points:**
- **Unsupervised** — no labeled data needed
- Principle: anomalies are "few and different" — easier to isolate
- Training: O(n · t · log ψ) — done offline once
- Scoring: O(t · log ψ) — per event in real-time
- Features: temperature, humidity, pressure, vibration
- StandardScaler normalization
- Contamination: 0.05 (5%)
- Saved with joblib for fast loading

**What to say:**
> "Isolation Forest works by building random trees. Normal points require many splits to isolate; anomalies need few splits. This is perfect for streaming because scoring each event is fast."

---

## Slide 12: Database (Layer 5)

**Title:** Layer 5: MySQL Database — Serving Layer

**Bullet Points:**
- `sensor_readings` table: every processed event with rolling metrics and anomaly scores
- `sensor_metrics` table: per-device aggregated statistics (upserted in real-time)
- Indexed on device_id, timestamp, is_anomaly
- Connection pooling for concurrent access
- Serves as the bridge between processor and dashboard

**What to say:**
> "MySQL acts as our serving layer. The processor writes to it, and the dashboard reads from it. The sensor_metrics table provides fast per-device summaries without scanning all readings."

---

## Slide 13: Dashboard (Layer 6)

**Title:** Layer 6: Streamlit Dashboard — Live Monitoring

**Bullet Points:**
- Auto-refreshes every 3 seconds (configurable)
- KPI cards: temperature, humidity, pressure, vibration, totals
- Live temperature chart (Plotly)
- Rolling average vs actual values
- Anomaly visualization (normal=green, anomaly=red)
- Device filter (sidebar)
- Top anomalies table (from heap tracker)
- Recent events table
- Sensor status: NORMAL / WARNING / CRITICAL

**What to say:**
> "The dashboard reads from MySQL and auto-refreshes. It's not a static page — you can see data appearing in real-time as the producer streams events."

---

## Slide 14: Results & Demo

**Title:** Results & Live Demonstration

**Bullet Points:**
- Successfully processes 5000+ events through the complete pipeline
- ~5% anomaly detection rate matching injection rate
- All 30 unit tests passing
- Per-event processing in O(1) amortized time
- Dashboard updates in real-time
- Proof of genuine streaming: stopping producer freezes dashboard

**What to say:**
> "Let me show you the live demo. [Switch to demo] You can see data flowing through the pipeline. When I stop the producer, the dashboard freezes — proving this is real streaming, not a pre-loaded animation."

---

## Slide 15: Conclusion

**Title:** Conclusion & Future Scope

**Conclusion:**
- Successfully built a complete six-layer DSA pipeline
- Demonstrated efficient DSA data structures for streaming
- Achieved real-time anomaly detection with Isolation Forest
- Professional dashboard with genuine streaming visualization

**Future Scope:**
- Apache Flink/Spark for distributed processing
- Multiple ML algorithms (SVM, K-Means)
- Alerting system (email/SMS)
- Edge computing integration
- Time-series database (InfluxDB)

**What to say:**
> "We've successfully demonstrated all six layers of a DSA pipeline with efficient data structures. The system processes each event in constant time and scales well. Future work could add distributed processing and real-time alerting."

---

## Slide 16: Q&A

**Title:** Questions?

**Bullet Points:**
- Architecture: 6-layer streaming pipeline
- Streaming: Apache Kafka
- DSA: Deque, Dictionary, Heap, Running Statistics
- ML: Isolation Forest
- Database: MySQL
- Dashboard: Streamlit + Plotly

**What to say:**
> "Thank you! I'm happy to answer any questions about the architecture, DSA concepts, or implementation details."
