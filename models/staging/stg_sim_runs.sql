select
    trace, policy_id, scenario_id, block_gb, kv_bytes_per_token, unlimited,
    capacity_blocks_hbm, capacity_blocks_dram, capacity_blocks_ssd, capacity_blocks_hdd,
    blocks_written_hbm, blocks_written_dram, blocks_written_ssd, blocks_written_hdd,
    blocks_resident_hbm, blocks_resident_dram, blocks_resident_ssd, blocks_resident_hdd,
    blocks_dropped, requests
from {{ source('raw_sim', 'runs') }}
