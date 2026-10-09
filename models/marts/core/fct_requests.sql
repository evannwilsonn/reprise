-- Every simulated request, next to the same request with no reuse at all (same scenario, same trace).
select
    s.*,
    s.cached_tokens * 1.0 / nullif(s.input_tokens, 0)        as cached_share,
    b.ttft_ms                                                as recompute_ttft_ms,
    b.gpu_seconds                                            as recompute_gpu_seconds,
    1 - s.ttft_ms / nullif(b.ttft_ms, 0)                     as ttft_reduction
from {{ ref('stg_sim_requests') }} s
join {{ ref('stg_sim_requests') }} b
  on b.policy_id = 'recompute' and b.scenario_id = s.scenario_id and b.trace = s.trace and b.request_idx = s.request_idx
