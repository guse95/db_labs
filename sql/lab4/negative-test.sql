drop index if exists idx_tickets_status;

explain analyze
select *
from tickets
where status != 'закрыт';

create index idx_tickets_status
    on tickets(status);

analyze tickets;

explain analyze
select *
from tickets
where status != 'закрыт';

drop index if exists idx_tickets_status;