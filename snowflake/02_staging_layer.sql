-- ============================================================================
-- AtmoSync Snowflake Architecture: 02 - STAGING Layer (Cleaned & Flattened)
-- ============================================================================

USE DATABASE ATMOSYNC_DB;
USE SCHEMA STAGING_SCHEMA;

-- Staging View: Flattened and Type-Casted IoT Telemetry
CREATE OR REPLACE VIEW STG_TELEMETRY AS
SELECT
    INGESTION_ID,
    INGESTION_TIMESTAMP,
    PAYLOAD:event_id::VARCHAR(64) AS EVENT_ID,
    PAYLOAD:container_id::VARCHAR(32) AS CONTAINER_ID,
    PAYLOAD:shipment_id::VARCHAR(32) AS SHIPMENT_ID,
    PAYLOAD:timestamp::TIMESTAMP_NTZ AS RECORDED_AT,
    PAYLOAD:commodity::VARCHAR(50) AS COMMODITY_NAME,
    PAYLOAD:temperature::FLOAT AS TEMPERATURE_CELSIUS,
    PAYLOAD:humidity::FLOAT AS HUMIDITY_PERCENT,
    PAYLOAD:door_open::BOOLEAN AS DOOR_OPEN_STATUS,
    PAYLOAD:battery_pct::FLOAT AS BATTERY_PERCENT,
    PAYLOAD:gps_speed_kmh::FLOAT AS GPS_SPEED_KMH,
    PAYLOAD:latitude::FLOAT AS LATITUDE,
    PAYLOAD:longitude::FLOAT AS LONGITUDE,
    PAYLOAD:ambient_weather::VARCHAR(100) AS AMBIENT_WEATHER,
    PAYLOAD:market_price::FLOAT AS SPOT_MARKET_PRICE,
    PAYLOAD:origin::VARCHAR(100) AS ORIGIN_PORT,
    PAYLOAD:destination::VARCHAR(100) AS DESTINATION_PORT,
    PAYLOAD:remaining_distance_km::FLOAT AS REMAINING_DISTANCE_KM,
    PAYLOAD:eta_hours::FLOAT AS ETA_HOURS
FROM ATMOSYNC_DB.RAW_SCHEMA.RAW_TELEMETRY
WHERE PAYLOAD:container_id IS NOT NULL;

-- Staged Cleaned Materialized Telemetry Table with Clustering Keys
CREATE OR REPLACE TABLE STG_CLEAN_TELEMETRY AS
SELECT * FROM STG_TELEMETRY;

ALTER TABLE STG_CLEAN_TELEMETRY CLUSTER BY (RECORDED_AT::DATE, CONTAINER_ID);
