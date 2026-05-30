begin isolation level repeatable read;

select status
from tickets
where id = 1;

begin;
update tickets
set status = 'решен'
where id = 1;
commit;

select status
from tickets
where id = 1;

commit