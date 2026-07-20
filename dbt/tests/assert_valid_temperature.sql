-- Custom dbt test: Asserts temperature reading is within physical limits (-50C to +60C)
SELECT
    container_id,
    temperature_celsius,
    recorded_at
FROM {{ ref('stg_telemetry') }}
WHERE temperature_celsius < -50.0 OR temperature_celsius > 60.0
