-- hardware.csv as one row, so models can join to it
select
    max(case when item = 'gpus_per_node' then value end)         as gpus_per_node,
    max(case when item = 'nodes' then value end)                 as nodes,
    max(case when item = 'gpu_peak_tflops' then value end)       as gpu_peak_tflops,
    max(case when item = 'prefill_mfu' then value end)           as prefill_mfu,
    max(case when item = 'gpu_hour_cost' then value end)         as gpu_hour_cost,
    max(case when item = 'gpu_watts' then value end)             as gpu_watts
from {{ ref('hardware') }}
