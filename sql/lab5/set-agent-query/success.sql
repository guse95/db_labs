begin;

update tickets
set agent_id = 1,
    status = 'в работе'
where id = 1;

commit;

select * from tickets where id = 1;