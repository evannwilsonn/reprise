-- One row per trace x policy x scenario, with the per-hour economics of serving that trace.
-- Storage cost = purchase price of the tiers the policy uses, written off over amortisation_months.
with agg as (
    select trace, policy_id, scenario_id,
           count(*) as requests,
           sum(input_tokens) as input_tokens, sum(cached_tokens) as cached_tokens,
           sum(hits_hbm) as hits_hbm, sum(hits_dram) as hits_dram, sum(hits_ssd) as hits_ssd, sum(hits_hdd) as hits_hdd,
           sum(hits_recomputed_instead) as hits_recomputed_instead,
           avg(ttft_ms) as mean_ttft_ms,
           {{ pctl('ttft_ms', 0.5) }} as p50_ttft_ms,
           {{ pctl('ttft_ms', 0.95) }} as p95_ttft_ms,
           sum(gpu_seconds) as gpu_seconds,
           sum(load_ms) / 1000.0 as load_seconds
    from {{ ref('stg_sim_requests') }}
    group by 1, 2, 3
),
storage as (   -- provisioned capacity of the tiers a policy uses (GPU memory is part of the GPU price)
    select p.policy_id, sc.scenario_id,
           sum(t.capacity_gb_per_node * h.nodes * case t.tier when 'hbm' then sc.hbm_scale when 'dram' then sc.dram_scale
               when 'ssd' then sc.ssd_scale else sc.hdd_scale end * t.purchase_usd_per_gb)
               / {{ var('amortisation_months') }} / {{ var('hours_per_month') }} as storage_usd_per_hour
    from {{ ref('policies') }} p
    cross join {{ ref('scenarios') }} sc
    cross join {{ ref('int_hardware') }} h
    join {{ ref('tiers') }} t on position(t.tier in coalesce(p.tiers_used, '')) > 0
    where not p.unlimited
    group by 1, 2
)
select
    a.*,
    p.policy_name, p.policy_order, p.unlimited,
    sc.scenario_name,
    a.cached_tokens * 1.0 / nullif(a.input_tokens, 0)                     as cached_share,
    sp.span_hours,
    a.gpu_seconds / 3600.0 / sp.span_hours                                as gpu_hours_per_hour,
    a.gpu_seconds / 3600.0 * h.gpu_hour_cost / sp.span_hours              as gpu_usd_per_hour,
    a.gpu_seconds * h.gpu_watts / 3.6e6 / sp.span_hours                   as gpu_kwh_per_hour,
    case when p.unlimited then null else coalesce(st.storage_usd_per_hour, 0) end as storage_usd_per_hour,
    r.blocks_written_ssd * r.block_gb / 1000.0 / sp.span_hours            as ssd_tb_written_per_hour,
    r.blocks_written_hdd * r.block_gb / 1000.0 / sp.span_hours            as hdd_tb_written_per_hour,
    -- drive-writes per day: TB written per day / TB of SSD provisioned (endurance is rated in these units)
    case when position('ssd' in coalesce(p.tiers_used, '')) > 0 and not p.unlimited and sc.ssd_scale > 0
         then r.blocks_written_ssd * r.block_gb / sp.span_hours * 24
              / (ssd.capacity_gb_per_node * h.nodes * sc.ssd_scale) end    as ssd_drive_writes_per_day,
    ssd.rated_drive_writes_per_day                                        as ssd_rated_drive_writes_per_day,
    r.blocks_dropped, r.block_gb
from agg a
join {{ ref('policies') }} p on p.policy_id = a.policy_id
join {{ ref('scenarios') }} sc on sc.scenario_id = a.scenario_id
join {{ ref('int_trace_spans') }} sp on sp.trace = a.trace
join {{ ref('stg_sim_runs') }} r on r.trace = a.trace and r.policy_id = a.policy_id and r.scenario_id = a.scenario_id
cross join {{ ref('int_hardware') }} h
cross join (select * from {{ ref('tiers') }} where tier = 'ssd') ssd
left join storage st on st.policy_id = a.policy_id and st.scenario_id = a.scenario_id
