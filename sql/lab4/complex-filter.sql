drop index if exists idx_tickets_status_created;

explain analyze
select *
from tickets
where status = 'открыт'
  and created_at > now() - interval '30 days';

create index idx_tickets_status_created
    on tickets(status, created_at);

analyze tickets;

explain analyze
select *
from tickets
where status = 'открыт'
  and created_at > now() - interval '30 days';

drop index if exists idx_tickets_status_created;