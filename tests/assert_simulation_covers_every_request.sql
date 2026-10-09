-- Each simulation replayed every request of its trace exactly once, in the trace's own order.
select s.scenario_id, s.policy_id, s.trace, count(*) as simulated, max(t.requests) as in_trace
from {{ ref('stg_sim_requests') }} s
join {{ ref('int_trace_spans') }} t on t.trace = s.trace
group by 1, 2, 3
having count(*) <> max(t.requests)
union all
select s.scenario_id, s.policy_id, s.trace, 1, 0
from {{ ref('stg_sim_requests') }} s
join {{ ref('stg_trace_requests') }} t on t.trace = s.trace and t.request_idx = s.request_idx
where s.input_tokens <> t.input_tokens or s.timestamp_ms <> t.timestamp_ms or s.blocks <> t.blocks
