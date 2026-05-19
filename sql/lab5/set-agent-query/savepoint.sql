begin;

update tickets
set agent_id = 2
where id = 1;

savepoint before_status_change;

update tickets
set status = 'неверный статус'
where id = 1;

rollback to savepoint before_status_change;

update tickets
set status = 'в работе'
where id = 1;

commit;

select agent_id, status
from tickets
where id = 1;