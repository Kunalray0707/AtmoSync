{{ config(materialized='table') }}

WITH stg AS (
    SELECT * FROM {{ ref('stg_telemetry') }}
)

SELECT
    event_id,
    container_id,
    recorded_at,
    commodity_name,
    temperature_celsius,
    humidity_percent,
    door_open_status,
    CASE
        WHEN temperature_celsius > 8.0 THEN 'HIGH_EXCURSION'
        WHEN temperature_celsius > 5.5 THEN 'MODERATE_EXCURSION'
        ELSE 'NORMAL'
    END AS thermal_status,
    CASE
        WHEN door_open_status = TRUE THEN 'BREACH_ALERT'
        WHEN temperature_celsius > 8.0 THEN 'SPOILAGE_WARNING'
        ELSE 'OPTIMAL'
    END AS alert_severity
FROM stg
