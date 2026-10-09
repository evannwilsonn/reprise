-- How much wall-clock traffic each trace covers, to turn totals into per-hour rates.
select trace, count(*) as requests, sum(input_tokens) as input_tokens,
       (max(timestamp_ms) - min(timestamp_ms)) / 3600000.0 as span_hours
from {{ ref('stg_trace_requests') }}
group by 1
