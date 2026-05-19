begin isolation level serializable;

select status
from tickets
where id = 1;

begin isolation level serializable;

update tickets
set status = 'решен'
where id = 1;

commit;

select status
from tickets
where id = 1;

commit