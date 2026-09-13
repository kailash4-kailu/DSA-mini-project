"""
Top-N Anomaly Tracker (Heap-based)
====================================
Maintains the top N most anomalous sensor readings using a min-heap.

DSA Concept: Heap / Priority Queue (heapq)
---------------------------------------------
We use Python's heapq module (min-heap) to efficiently track the top N
highest-severity anomalies without sorting all readings.

Strategy:
  • We want the TOP N most anomalous readings.
  • Isolation Forest's decision_function returns lower scores for more
    anomalous readings (more negative = worse).
  • We use a MIN-HEAP of size N keyed on anomaly_score.
  • When a new anomaly arrives:
      – If heap has fewer than N items, push it.  O(log n)
      – Else if the new score < heap[0] (more anomalous than the least
        anomalous in our top-N), replace the root.  O(log n)
  • The heap always contains the N most anomalous readings.

Complexity Analysis:
  Operation              | Time     | Space
  -----------------------+----------+------
  Insert into heap       | O(log N) | O(N)
  Replace root           | O(log N) | O(N)
  Peek at root           | O(1)     | –
  Get all top-N (sorted) | O(N log N) | O(N)
  Space                  | O(N)     | –

  Where N = max number of top anomalies to track (e.g. 20).
  This is extremely efficient compared to sorting the entire stream.
"""

import heapq
from typing import Optional


class AnomalyTracker:
    """
    Heap-based tracker for the top N most anomalous sensor events.

    Parameters
    ----------
    max_size : int
        Maximum number of top anomalies to keep (default 20).
    """

    def __init__(self, max_size: int = 20):
        self._max_size = max_size
        # Min-heap of (score, sequence_number, reading_dict)
        # score is the anomaly_score from IsolationForest (lower = more anomalous)
        self._heap: list[tuple[float, int, dict]] = []
        self._seq = 0  # tie-breaker for equal scores

    def add(self, anomaly_score: float, reading: dict) -> None:
        """
        Consider adding a reading to the top-N anomalies.

        Since lower scores are more anomalous and we want to keep the N
        lowest scores, we use a MAX-heap on score (negate to use min-heap),
        or equivalently a min-heap on score and keep the N smallest.

        Actually, let's keep it simple:
        We store (anomaly_score, seq, reading) in a min-heap.
        We always want the N LOWEST scores (most anomalous).
        So we use a MAX-heap by negating: store (-score, seq, reading).
        The root of the max-heap is the LEAST anomalous of our top-N.
        When the heap is full and a new item is MORE anomalous (lower score),
        we replace the root.

        Wait – simpler approach:
        Store (score, seq, reading) as-is in a MAX-heap (negate score).
        Actually let's just use a min-heap storing score directly.
        We want the N smallest scores.
        Use a max-heap of size N: negate scores, use heapq (min-heap on negated = max-heap).

        Clearest approach:
        - Use a max-heap of size N to keep the N smallest scores.
        - max-heap via min-heap trick: store negated scores.
        - Root = largest negated score = largest original score = least anomalous in our set.
        - When full, if new score < -heap[0], replace root.
        """
        self._seq += 1
        # We store (score, seq, reading) in a min-heap.
        # We want the N LOWEST scores.  Use a max-heap of size N.
        neg_score = -anomaly_score
        entry = (neg_score, self._seq, reading)

        if len(self._heap) < self._max_size:
            heapq.heappush(self._heap, entry)
        else:
            # heap[0] has the smallest neg_score = largest original score
            # = least anomalous in our top-N
            # A new reading is more anomalous if its score is lower,
            # i.e., neg_score is larger.
            if neg_score > self._heap[0][0]:
                heapq.heapreplace(self._heap, entry)

    def get_top_anomalies(self) -> list[dict]:
        """
        Return the top anomalies sorted from most to least anomalous.
        O(N log N) for the sort.
        """
        # Sort by neg_score descending (= original score ascending = most anomalous first)
        sorted_entries = sorted(self._heap, key=lambda x: x[0], reverse=True)
        results = []
        for neg_score, seq, reading in sorted_entries:
            entry = dict(reading)
            entry["anomaly_score"] = -neg_score
            results.append(entry)
        return results

    @property
    def size(self) -> int:
        return len(self._heap)

    def peek_threshold(self) -> Optional[float]:
        """Return the score of the least-anomalous entry in our top-N."""
        if not self._heap:
            return None
        return -self._heap[0][0]

    def clear(self) -> None:
        self._heap.clear()
        self._seq = 0
