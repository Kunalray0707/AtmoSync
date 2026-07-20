{{ config(materialized='view') }}

WITH raw_source AS (
    SELECT * FROM {{ source('raw_data', 'raw_telemetry') }}
)

SELECT
    INGESTION_ID,
    INGESTION_TIMESTAMP,
    PAYLOAD:event_id::VARCHAR(64) AS event_id,
    PAYLOAD:container_id::VARCHAR(32) AS container_id,
    PAYLOAD:shipment_id::VARCHAR(32) AS shipment_id,
    PAYLOAD:timestamp::TIMESTAMP_NTZ AS recorded_at,
    PAYLOAD:commodity::VARCHAR(50) AS commodity_name,
    PAYLOAD:temperature::FLOAT AS temperature_celsius,
    PAYLOAD:humidity::FLOAT AS humidity_percent,
    PAYLOAD:door_open::BOOLEAN AS door_open_status,
    PAYLOAD:battery_pct::FLOAT AS battery_percent,
    PAYLOAD:gps_speed_kmh::FLOAT AS gps_speed_kmh,
    PAYLOAD:latitude::FLOAT AS latitude,
    PAYLOAD:longitude::FLOAT AS longitude,
    PAYLOAD:ambient_weather::VARCHAR(100) AS ambient_weather,
    PAYLOAD:market_price::FLOAT AS spot_market_price
FROM raw_source
WHERE PAYLOAD:container_id IS NOT NULL
