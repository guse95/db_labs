begin;

update tickets
set status = 'решен'
where id = 1;

insert into knowledge_for_ticket(ticket_id, knowledge_id)
values (1, 999);

rollback;

select status
from tickets
where id = 1;