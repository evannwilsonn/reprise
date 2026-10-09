-- Unlimited GPU memory is the most reuse a trace allows; no real policy can cache more.
select p.scenario_id, p.trace, p.policy_id, p.cached_share, c.cached_share as ceiling
from {{ ref('fct_simulations') }} p
join {{ ref('fct_simulations') }} c on c.trace = p.trace and c.scenario_id = p.scenario_id and c.policy_id = 'ceiling'
where p.cached_share > c.cached_share + 1e-9
