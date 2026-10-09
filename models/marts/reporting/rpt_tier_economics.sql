-- For each tier: what one 512-token block costs to fetch versus to recompute, so it is visible
-- when a tier is worth reading from at all. Recompute is shown at the start of a prompt and
-- 12,000 tokens in, where attention makes each block more expensive.
with h as (select * from {{ ref('int_hardware') }}),
m as (select *, 2.0 * layers * kv_heads * head_dim * kv_bytes_per_value * {{ var('block_tokens') }} / 1e9 as block_gb
      from {{ ref('model_profile') }}),
node as (select gpus_per_node * gpu_peak_tflops * 1e12 * prefill_mfu as node_flops from h)
select
    m.model_id, m.model_name, m.block_gb,
    t.tier, t.tier_order, t.tier_name, t.capacity_gb_per_node, t.read_gb_s_per_node, t.access_latency_ms, t.purchase_usd_per_gb,
    case when t.tier = 'hbm' then 0.05 else t.access_latency_ms + m.block_gb / t.read_gb_s_per_node * 1000 end as fetch_ms,
    (2 * m.parameters_b * 1e9 * {{ var('block_tokens') }} + 2.0 * m.layers * m.hidden_size * power({{ var('block_tokens') }}, 2)) / n.node_flops * 1000 as recompute_ms_at_start,
    (2 * m.parameters_b * 1e9 * {{ var('block_tokens') }} + 2.0 * m.layers * m.hidden_size * (power(12000 + {{ var('block_tokens') }}, 2) - power(12000, 2))) / n.node_flops * 1000 as recompute_ms_at_12k,
    floor(t.capacity_gb_per_node / m.block_gb) as blocks_per_node,
    t.source_note
from m cross join {{ ref('tiers') }} t cross join node n
