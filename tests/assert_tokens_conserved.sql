-- Every input token is either reused from cache or computed, never both, never neither.
select scenario_id, policy_id, trace, request_idx
from {{ ref('stg_sim_requests') }}
where cached_tokens + computed_tokens <> input_tokens or cached_tokens < 0
