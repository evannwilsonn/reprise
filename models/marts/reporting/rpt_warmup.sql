-- Minute by minute: how the cache fills up and what that does to latency (reference cluster).
select
    scenario_id, policy_id, trace,
    cast(floor(timestamp_ms / 60000) as integer) as minute,
    count(*) as requests,
    sum(cached_tokens) * 1.0 / sum(input_tokens) as cached_share,
    avg(ttft_ms) as mean_ttft_ms
from {{ ref('stg_sim_requests') }}
where scenario_id in ('base', 'memory_pressure')
group by 1, 2, 3, 4
