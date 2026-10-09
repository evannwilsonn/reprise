-- Independent check of the simulator's maths: with nothing cached, prefill time must equal
-- 2*params*n + 2*layers*hidden*n^2 FLOPs at the stated node throughput (to within rounding).
with h as (select * from {{ ref('int_hardware') }}),
m as (select * from {{ ref('model_profile') }} where model_id = 'llama31_70b_fp16')
select s.trace, s.request_idx, s.compute_ms,
       (2 * m.parameters_b * 1e9 * s.input_tokens + 2.0 * m.layers * m.hidden_size * power(s.input_tokens, 2))
         / (h.gpus_per_node * h.gpu_peak_tflops * 1e12 * h.prefill_mfu) * 1000 as expected_ms
from {{ ref('stg_sim_requests') }} s cross join h cross join m
where s.policy_id = 'recompute' and s.scenario_id = 'base'
  and abs(s.compute_ms - (2 * m.parameters_b * 1e9 * s.input_tokens + 2.0 * m.layers * m.hidden_size * power(s.input_tokens, 2))
         / (h.gpus_per_node * h.gpu_peak_tflops * 1e12 * h.prefill_mfu) * 1000) > 0.01
