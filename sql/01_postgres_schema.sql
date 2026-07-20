-- ============================================================================
-- ATMOSYNC POSTGRESQL OPERATIONAL DATABASE SCHEMA
-- ============================================================================

CREATE TABLE IF NOT EXISTS container_telemetry (
    id BIGSERIAL PRIMARY KEY,
    container_id VARCHAR(64) NOT NULL,
    shipment_id VARCHAR(64) NOT NULL,
    recorded_at TIMESTAMP WITH TIME ZONE NOT NULL,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    commodity VARCHAR(64) NOT NULL,
    temperature DOUBLE PRECISION NOT NULL,
    humidity DOUBLE PRECISION NOT NULL,
    door_open BOOLEAN DEFAULT FALSE,
    battery DOUBLE PRECISION,
    gps_speed DOUBLE PRECISION,
    ambient_temperature DOUBLE PRECISION,
    market_price DOUBLE PRECISION,
    destination VARCHAR(128),
    origin VARCHAR(128),
    remaining_distance_km DOUBLE PRECISION,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_telemetry_container_time ON container_telemetry (container_id, recorded_at DESC);
CREATE INDEX IF NOT EXISTS idx_telemetry_commodity ON container_telemetry (commodity);

CREATE TABLE IF NOT EXISTS alerts_log (
    alert_id VARCHAR(64) PRIMARY KEY,
    container_id VARCHAR(64) NOT NULL,
    shipment_id VARCHAR(64),
    severity VARCHAR(32) NOT NULL,
    alert_type VARCHAR(64) NOT NULL,
    message TEXT NOT NULL,
    raised_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved BOOLEAN DEFAULT FALSE
);
