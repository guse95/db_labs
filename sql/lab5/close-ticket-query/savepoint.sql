begin;

update tickets
set status = 'закрыт'
where id = 1;

savepoint remove_agent;

update tickets
set client_id = 999
where id = 1;

rollback to savepoint remove_agent;

update tickets
set agent_id = null
where id = 1;

commit;