-- dbt Mart Model: fct_arbitrage_opportunities.sql
{{ config(materialized='table') }}

with spoilage as (
    select * from {{ ref('fct_spoilage_events') }}
)

select
    s.container_id,
    s.shipment_id,
    s.recorded_at,
    s.commodity,
    s.spoilage_risk_score_pct,
    s.spoilage_category,
    -- Arbitrage Financial Delta logic
    case
        when s.spoilage_risk_score_pct >= 50.0 then 4850.00
        when s.spoilage_risk_score_pct >= 25.0 then 2100.00
        else 0.00
    end as max_net_profit_delta_usd,
    case
        when s.spoilage_risk_score_pct >= 50.0 then 'REROUTE_RECOMMENDED'
        else 'MAINTAIN_CURRENT_ROUTE'
    end as arbitrage_decision
from spoilage s
