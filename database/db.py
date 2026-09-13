"""
Database helper module.
Provides connection pooling and common query functions for MySQL.
"""
import os
import logging
import mysql.connector
from mysql.connector import pooling, Error
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Connection pool (singleton)
# ---------------------------------------------------------------------------
_pool = None


def get_pool():
    """Return a connection pool, creating it on first call."""
    global _pool
    if _pool is None:
        try:
            _pool = pooling.MySQLConnectionPool(
                pool_name="iot_pool",
                pool_size=5,
                host=os.getenv("MYSQL_HOST", "localhost"),
                port=int(os.getenv("MYSQL_PORT", 3306)),
                database=os.getenv("MYSQL_DATABASE", "iot_streaming"),
                user=os.getenv("MYSQL_USER", "root"),
                password=os.getenv("MYSQL_PASSWORD", "changeme_secret"),
                autocommit=True,
            )
            logger.info("MySQL connection pool created.")
        except Error as e:
            logger.error("Failed to create MySQL pool: %s", e)
            raise
    return _pool


def get_connection():
    """Get a connection from the pool."""
    return get_pool().get_connection()


# ---------------------------------------------------------------------------
# Insert helpers
# ---------------------------------------------------------------------------

def insert_reading(data: dict):
    """Insert a processed sensor reading row."""
    sql = """
        INSERT INTO sensor_readings
            (timestamp, device_id, temperature, humidity, pressure, vibration,
             rolling_temperature, rolling_humidity, rolling_pressure, rolling_vibration,
             anomaly_score, is_anomaly, processed_at)
        VALUES
            (%(timestamp)s, %(device_id)s, %(temperature)s, %(humidity)s,
             %(pressure)s, %(vibration)s,
             %(rolling_temperature)s, %(rolling_humidity)s,
             %(rolling_pressure)s, %(rolling_vibration)s,
             %(anomaly_score)s, %(is_anomaly)s, NOW(3))
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        cursor.close()
    except Error as e:
        logger.error("insert_reading error: %s", e)
        raise
    finally:
        if conn:
            conn.close()


def upsert_metrics(data: dict):
    """Insert or update per-device aggregate metrics."""
    sql = """
        INSERT INTO sensor_metrics
            (device_id, total_readings, anomaly_count,
             latest_temperature, latest_humidity, latest_pressure, latest_vibration,
             avg_temperature, avg_humidity, avg_pressure, avg_vibration,
             min_temperature, max_temperature,
             min_humidity, max_humidity,
             min_pressure, max_pressure,
             min_vibration, max_vibration,
             latest_anomaly_score, updated_at)
        VALUES
            (%(device_id)s, %(total_readings)s, %(anomaly_count)s,
             %(latest_temperature)s, %(latest_humidity)s, %(latest_pressure)s, %(latest_vibration)s,
             %(avg_temperature)s, %(avg_humidity)s, %(avg_pressure)s, %(avg_vibration)s,
             %(min_temperature)s, %(max_temperature)s,
             %(min_humidity)s, %(max_humidity)s,
             %(min_pressure)s, %(max_pressure)s,
             %(min_vibration)s, %(max_vibration)s,
             %(latest_anomaly_score)s, NOW(3))
        ON DUPLICATE KEY UPDATE
            total_readings      = VALUES(total_readings),
            anomaly_count       = VALUES(anomaly_count),
            latest_temperature  = VALUES(latest_temperature),
            latest_humidity     = VALUES(latest_humidity),
            latest_pressure     = VALUES(latest_pressure),
            latest_vibration    = VALUES(latest_vibration),
            avg_temperature     = VALUES(avg_temperature),
            avg_humidity        = VALUES(avg_humidity),
            avg_pressure        = VALUES(avg_pressure),
            avg_vibration       = VALUES(avg_vibration),
            min_temperature     = VALUES(min_temperature),
            max_temperature     = VALUES(max_temperature),
            min_humidity        = VALUES(min_humidity),
            max_humidity        = VALUES(max_humidity),
            min_pressure        = VALUES(min_pressure),
            max_pressure        = VALUES(max_pressure),
            min_vibration       = VALUES(min_vibration),
            max_vibration       = VALUES(max_vibration),
            latest_anomaly_score = VALUES(latest_anomaly_score),
            updated_at          = NOW(3)
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        cursor.close()
    except Error as e:
        logger.error("upsert_metrics error: %s", e)
        raise
    finally:
        if conn:
            conn.close()


# ---------------------------------------------------------------------------
# Query helpers (used by dashboard)
# ---------------------------------------------------------------------------

def fetch_recent_readings(device_id: str = None, limit: int = 200):
    """Return the most recent sensor readings, optionally filtered by device."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        if device_id and device_id != "All":
            cursor.execute(
                "SELECT * FROM sensor_readings WHERE device_id=%s ORDER BY id DESC LIMIT %s",
                (device_id, limit),
            )
        else:
            cursor.execute(
                "SELECT * FROM sensor_readings ORDER BY id DESC LIMIT %s",
                (limit,),
            )
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except Error as e:
        logger.error("fetch_recent_readings error: %s", e)
        return []
    finally:
        if conn:
            conn.close()


def fetch_metrics():
    """Return all per-device metric rows."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM sensor_metrics ORDER BY device_id")
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except Error as e:
        logger.error("fetch_metrics error: %s", e)
        return []
    finally:
        if conn:
            conn.close()


def fetch_top_anomalies(limit: int = 10):
    """Return the top anomaly-score readings."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM sensor_readings WHERE is_anomaly=1 ORDER BY anomaly_score ASC LIMIT %s",
            (limit,),
        )
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except Error as e:
        logger.error("fetch_top_anomalies error: %s", e)
        return []
    finally:
        if conn:
            conn.close()


def fetch_device_ids():
    """Return distinct device IDs from the readings table."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT device_id FROM sensor_readings ORDER BY device_id")
        rows = [r[0] for r in cursor.fetchall()]
        cursor.close()
        return rows
    except Error as e:
        logger.error("fetch_device_ids error: %s", e)
        return []
    finally:
        if conn:
            conn.close()


def fetch_total_counts():
    """Return total readings and total anomalies."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT COUNT(*) as total, SUM(is_anomaly) as anomalies FROM sensor_readings"
        )
        row = cursor.fetchone()
        cursor.close()
        return row
    except Error as e:
        logger.error("fetch_total_counts error: %s", e)
        return {"total": 0, "anomalies": 0}
    finally:
        if conn:
            conn.close()
