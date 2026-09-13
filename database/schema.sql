-- ============================================================
-- IoT Streaming Analytics - Database Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS iot_streaming;
USE iot_streaming;

-- Main table: all processed sensor readings
CREATE TABLE IF NOT EXISTS sensor_readings (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    timestamp       DATETIME(3)    NOT NULL,
    device_id       VARCHAR(32)    NOT NULL,
    temperature     DOUBLE         NOT NULL,
    humidity        DOUBLE         NOT NULL,
    pressure        DOUBLE         NOT NULL,
    vibration       DOUBLE         NOT NULL,
    rolling_temperature DOUBLE     DEFAULT NULL,
    rolling_humidity    DOUBLE     DEFAULT NULL,
    rolling_pressure    DOUBLE     DEFAULT NULL,
    rolling_vibration   DOUBLE     DEFAULT NULL,
    anomaly_score   DOUBLE         DEFAULT NULL,
    is_anomaly      TINYINT(1)     DEFAULT 0,
    processed_at    DATETIME(3)    NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    INDEX idx_device   (device_id),
    INDEX idx_ts       (timestamp),
    INDEX idx_anomaly  (is_anomaly),
    INDEX idx_device_ts (device_id, timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Aggregated per-device metrics (updated in real-time)
CREATE TABLE IF NOT EXISTS sensor_metrics (
    device_id           VARCHAR(32)  PRIMARY KEY,
    total_readings      BIGINT       DEFAULT 0,
    anomaly_count       BIGINT       DEFAULT 0,
    latest_temperature  DOUBLE       DEFAULT NULL,
    latest_humidity     DOUBLE       DEFAULT NULL,
    latest_pressure     DOUBLE       DEFAULT NULL,
    latest_vibration    DOUBLE       DEFAULT NULL,
    avg_temperature     DOUBLE       DEFAULT NULL,
    avg_humidity        DOUBLE       DEFAULT NULL,
    avg_pressure        DOUBLE       DEFAULT NULL,
    avg_vibration       DOUBLE       DEFAULT NULL,
    min_temperature     DOUBLE       DEFAULT NULL,
    max_temperature     DOUBLE       DEFAULT NULL,
    min_humidity        DOUBLE       DEFAULT NULL,
    max_humidity        DOUBLE       DEFAULT NULL,
    min_pressure        DOUBLE       DEFAULT NULL,
    max_pressure        DOUBLE       DEFAULT NULL,
    min_vibration       DOUBLE       DEFAULT NULL,
    max_vibration       DOUBLE       DEFAULT NULL,
    latest_anomaly_score DOUBLE      DEFAULT NULL,
    updated_at          DATETIME(3)  NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
