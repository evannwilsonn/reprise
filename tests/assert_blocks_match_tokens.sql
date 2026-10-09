-- Mooncake hashes every 512 tokens of a prompt, so a request's block count is fixed by its length.
select trace, request_idx, input_tokens, blocks
from {{ ref('stg_trace_requests') }}
where blocks <> cast(ceil(input_tokens / 512.0) as integer)
