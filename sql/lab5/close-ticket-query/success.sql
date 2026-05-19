begin;

update tickets
set status = 'закрыт',
    agent_id = null
where id = 1;

commit;

select status from tickets where id = 1;