drop index if exists idx_agent;
drop index if exists idx_agent_status;

explain analyze
select *
from tickets
where agent_id = 10
  and status = 'в работе';

create index idx_agent
    on tickets(agent_id);

analyze tickets;

explain analyze
select *
from tickets
where agent_id = 10
  and status = 'в работе';

drop index if exists idx_agent;

create index idx_agent_status
    on tickets(agent_id, status);

analyze tickets;

explain analyze
select *
from tickets
where agent_id = 10
  and status = 'в работе';

drop index if exists idx_agent_status;