-- How much faster the first token arrives, by how much of the request's context was reusable.
-- This is the like-for-like comparison with "reuse vs regenerate" benchmarks.
select
    scenario_id, policy_id, trace,
    case when cached_share = 0 then '0%' when cached_share < 0.25 then '1-25%' when cached_share < 0.5 then '25-50%'
         when cached_share < 0.75 then '50-75%' when cached_share < 0.9 then '75-90%' else '90-100%' end as cached_band,
    min(cached_share) as band_floor,
    count(*) as requests,
    avg(ttft_ms) as mean_ttft_ms,
    avg(recompute_ttft_ms) as mean_recompute_ttft_ms,
    1 - avg(ttft_ms) / nullif(avg(recompute_ttft_ms), 0) as ttft_reduction
from {{ ref('fct_requests') }}
where policy_id <> 'recompute'
group by 1, 2, 3, 4
