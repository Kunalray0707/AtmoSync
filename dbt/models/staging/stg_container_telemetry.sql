-- dbt Staging Model: stg_container_telemetry.sql
{{ config(materialized='view') }}

with source_data as (
    select * from {{ source('raw', 'RAW_CONTAINER_TELEMETRY') }}
)

select
    RAW_PAYLOAD:container_id::varchar(64) as container_id,
    RAW_PAYLOAD:shipment_id::varchar(64) as shipment_id,
    RAW_PAYLOAD:timestamp::timestamp_ntz as recorded_at,
    RAW_PAYLOAD:latitude::float as latitude,
    RAW_PAYLOAD:longitude::float as longitude,
    RAW_PAYLOAD:commodity::varchar(64) as commodity,
    RAW_PAYLOAD:temperature::float as temperature,
    RAW_PAYLOAD:humidity::float as humidity,
    RAW_PAYLOAD:door_open::boolean as door_open,
    RAW_PAYLOAD:battery::float as battery_pct,
    RAW_PAYLOAD:gps_speed::float as gps_speed_kmh,
    RAW_PAYLOAD:ambient_temperature::float as ambient_temperature,
    RAW_PAYLOAD:market_price::float as market_price_usd,
    RAW_PAYLOAD:destination::varchar(128) as destination_port,
    RAW_PAYLOAD:origin::varchar(128) as origin_port,
    RAW_PAYLOAD:remaining_distance_km::float as remaining_distance_km,
    ingested_at
from source_data
where RAW_PAYLOAD:container_id is not null
