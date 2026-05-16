drop index if exists idx_tickets_created_at;

explain analyze
select *
from tickets
order by created_at desc
    limit 100;

create index idx_tickets_created_at
    on tickets(created_at desc);

analyze tickets;

explain analyze
select *
from tickets
where agent_id = 10
  and status = 'в работе';

drop index if exists idx_tickets_created_at;