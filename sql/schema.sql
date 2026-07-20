-- ============================================================================
-- AtmoSync PostgreSQL Relational Database Schema
-- ============================================================================

CREATE TABLE IF NOT EXISTS reefer_containers (
    container_id VARCHAR(32) PRIMARY KEY,
    commodity_type VARCHAR(50) NOT NULL,
    max_capacity_tonnes NUMERIC(10, 2) DEFAULT 25.0,
    optimum_temp_celsius NUMERIC(5, 2) NOT NULL,
    max_temp_celsius NUMERIC(5, 2) NOT NULL,
    min_temp_celsius NUMERIC(5, 2) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS telemetry_logs (
    event_id VARCHAR(64) PRIMARY KEY,
    container_id VARCHAR(32) REFERENCES reefer_containers(container_id),
    recorded_at TIMESTAMP WITH TIME ZONE NOT NULL,
    temperature_celsius NUMERIC(5, 2) NOT NULL,
    humidity_percent NUMERIC(5, 2) NOT NULL,
    door_open BOOLEAN DEFAULT FALSE,
    gps_speed_kmh NUMERIC(6, 2),
    latitude NUMERIC(9, 6),
    longitude NUMERIC(9, 6),
    spot_market_price NUMERIC(12, 2)
);

CREATE TABLE IF NOT EXISTS spoilage_alerts (
    alert_id SERIAL PRIMARY KEY,
    container_id VARCHAR(32) REFERENCES reefer_containers(container_id),
    alert_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    arrhenius_decay_ratio NUMERIC(6, 3),
    remaining_shelf_life_hours NUMERIC(8, 2),
    freshness_index_pct NUMERIC(5, 2),
    severity VARCHAR(20) NOT NULL
);

CREATE INDEX idx_telemetry_container_time ON telemetry_logs (container_id, recorded_at DESC);
