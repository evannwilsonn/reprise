select
    trace,
    cast(line_no as integer)                                   as request_idx,
    {{ jfield('payload', 'timestamp', 'bigint') }}             as timestamp_ms,
    {{ jfield('payload', 'input_length', 'integer') }}         as input_tokens,
    {{ jfield('payload', 'output_length', 'integer') }}        as output_tokens,
    {{ json_array_length('payload', 'hash_ids') }}             as blocks
from {{ source('raw_mooncake', 'requests') }}
