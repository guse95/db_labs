begin;

update tickets
set status = 'закрыт'
where id = 1;

update tickets
set client_id = 999
where id = 1;

commit;

rollback;