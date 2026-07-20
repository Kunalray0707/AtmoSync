-- ============================================================================
-- AtmoSync Advanced Analytical Queries (SQL CTEs & Window Functions)
-- ============================================================================

-- 1. Cumulative Thermal Excursion Hours per Container over past 24 Hours
WITH ExcursionEvents AS (
    SELECT
        container_id,
        recorded_at,
        temperature_celsius,
        CASE WHEN temperature_celsius > 8.0 THEN 1 ELSE 0 END AS is_excursion,
        LAG(recorded_at) OVER (PARTITION BY container_id ORDER BY recorded_at) AS prev_recorded_at
    FROM telemetry_logs
    WHERE recorded_at >= NOW() - INTERVAL '24 hours'
)
SELECT
    container_id,
    SUM(is_excursion) AS excursion_readings_count,
    COUNT(*) AS total_readings,
    ROUND(SUM(is_excursion)::NUMERIC / NULLIF(COUNT(*), 0) * 100, 2) AS excursion_time_pct
FROM ExcursionEvents
GROUP BY container_id
ORDER BY excursion_time_pct DESC;

-- 2. Destination Market Arbitrage Opportunity Ranking
WITH MarketPrices AS (
    SELECT
        container_id,
        commodity_type,
        spot_market_price AS current_market_price,
        FIRST_VALUE(spot_market_price) OVER (PARTITION BY commodity_type ORDER BY spot_market_price DESC) AS max_market_price
    FROM telemetry_logs
)
SELECT
    container_id,
    commodity_type,
    current_market_price,
    max_market_price,
    (max_market_price - current_market_price) AS potential_gain_per_ton
FROM MarketPrices
GROUP BY container_id, commodity_type, current_market_price, max_market_price
HAVING (max_market_price - current_market_price) > 200.0;
