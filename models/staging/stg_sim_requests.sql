select
    trace, policy_id, scenario_id,
    cast(request_idx as integer) as request_idx, timestamp_ms, input_tokens, output_tokens, blocks,
    prefix_blocks_cached, hits_hbm, hits_dram, hits_ssd, hits_hdd, hits_recomputed_instead,
    cached_tokens, computed_tokens, load_ms, compute_ms, ttft_ms, gpu_seconds
from {{ source('raw_sim', 'requests') }}
