-- Each policy against recomputing everything, per trace and scenario.
with s as (select * from {{ ref('fct_simulations') }}),
b as (select * from s where policy_id = 'recompute'),
c as (select trace, scenario_id, cached_share as ceiling_share from s where policy_id = 'ceiling')
select
    s.scenario_id, s.scenario_name, s.trace, s.policy_id, s.policy_name, s.policy_order, s.unlimited,
    s.requests, s.cached_share, c.ceiling_share,
    s.cached_share / nullif(c.ceiling_share, 0)                         as share_of_ceiling,
    s.mean_ttft_ms, s.p50_ttft_ms, s.p95_ttft_ms,
    1 - s.mean_ttft_ms / b.mean_ttft_ms                                 as mean_ttft_reduction,
    1 - s.p95_ttft_ms / b.p95_ttft_ms                                   as p95_ttft_reduction,
    s.gpu_hours_per_hour,
    b.gpu_hours_per_hour - s.gpu_hours_per_hour                         as gpu_hours_saved_per_hour,
    s.gpu_usd_per_hour, s.storage_usd_per_hour,
    b.gpu_usd_per_hour - s.gpu_usd_per_hour - coalesce(s.storage_usd_per_hour, 0) as net_usd_saved_per_hour,
    b.gpu_kwh_per_hour - s.gpu_kwh_per_hour                             as gpu_kwh_saved_per_hour,
    s.ssd_tb_written_per_hour, s.hdd_tb_written_per_hour, s.ssd_drive_writes_per_day, s.ssd_rated_drive_writes_per_day,
    s.hits_hbm, s.hits_dram, s.hits_ssd, s.hits_hdd, s.hits_recomputed_instead
from s
join b on b.trace = s.trace and b.scenario_id = s.scenario_id
join c on c.trace = s.trace and c.scenario_id = s.scenario_id
