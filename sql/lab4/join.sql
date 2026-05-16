drop index if exists idx_tickets_client;
drop index if exists idx_tickets_agent;
drop index if exists idx_tickets_status;

explain analyze
select
    t.id,
    c.client_name,
    a.agent_name
from tickets t
         join clients c on c.id = t.client_id
         join agents a on a.id = t.agent_id
where t.status = 'решен';

create index idx_tickets_client
    on tickets(client_id);

create index idx_tickets_agent
    on tickets(agent_id);

create index idx_tickets_status
    on tickets(status);

analyze tickets;

explain analyze
select
    t.id,
    c.client_name,
    a.agent_name
from tickets t
         join clients c on c.id = t.client_id
         join agents a on a.id = t.agent_id
where t.status = 'решен';

drop index if exists idx_tickets_client;
drop index if exists idx_tickets_agent;
drop index if exists idx_tickets_status;