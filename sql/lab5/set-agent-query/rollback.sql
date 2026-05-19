begin;

update tickets
set agent_id = 2
where id = 1;

update tickets
set status = 'ошибка'
where id = 1;

commit;

rollback;

select agent_id, status
from tickets
where id = 1;