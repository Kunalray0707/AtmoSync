-- ============================================================================
-- ATMOSYNC ADVANCED ANALYTICAL SQL QUERIES
-- High-performance window functions, rolling averages, and spoilage rollups
-- ============================================================================

-- Query 1: 1-Hour Rolling Thermal Drift and Sudden Temperature Excursion Spikes
SELECT
    container_id,
    commodity,
    recorded_at,
    temperature,
    AVG(temperature) OVER (
        PARTITION BY container_id
        ORDER BY recorded_at
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS rolling_avg_temp_1hr,
    temperature - LAG(temperature, 1) OVER (
        PARTITION BY container_id
        ORDER BY recorded_at
    ) AS temp_spike_delta
FROM container_telemetry
WHERE recorded_at >= NOW() - INTERVAL '24 hours'
ORDER BY container_id, recorded_at DESC;

-- Query 2: Commodity Spoiled Mass & Projected Financial Loss Rollup by Route
SELECT
    origin,
    destination,
    commodity,
    COUNT(DISTINCT container_id) AS total_containers,
    AVG(temperature) AS avg_temperature_celsius,
    SUM(CASE WHEN temperature > 8.0 THEN 1 ELSE 0 END) AS excursion_events,
    ROUND(SUM(CASE WHEN temperature > 8.0 THEN 20000 * market_price * 0.40 ELSE 0 END)::numeric, 2) AS projected_loss_usd
FROM container_telemetry
GROUP BY origin, destination, commodity
HAVING COUNT(DISTINCT container_id) > 0
ORDER BY projected_loss_usd DESC;
