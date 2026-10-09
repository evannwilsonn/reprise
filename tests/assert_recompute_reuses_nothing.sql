select scenario_id, trace, request_idx from {{ ref('stg_sim_requests') }}
where policy_id = 'recompute' and (cached_tokens > 0 or load_ms > 0)
