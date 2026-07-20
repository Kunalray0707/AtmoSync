-- dbt Test: assert_positive_shelf_life.sql
-- Fails if any spoilage risk score is less than 0 or greater than 100

select
    container_id,
    recorded_at,
    spoilage_risk_score_pct
from {{ ref('fct_spoilage_events') }}
where spoilage_risk_score_pct < 0.0 or spoilage_risk_score_pct > 100.0
