drop index if exists idx_tickets_status;

explain analyze
update tickets
set status = 'закрыт'
where status = 'открыт';

create index idx_tickets_status on tickets(status);
analyze tickets;

explain analyze
update tickets
set status = 'решен'
where status = 'закрыт';

drop index if exists idx_tickets_status;