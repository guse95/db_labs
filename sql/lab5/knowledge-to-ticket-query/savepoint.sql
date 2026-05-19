begin;

update tickets
set status = 'решен'
where id = 1;

savepoint kb_insert;

insert into knowledge_for_ticket(ticket_id, knowledge_id)
values (1, 999);

rollback to savepoint kb_insert;

insert into knowledge_for_ticket(ticket_id, knowledge_id)
values (1, 1);

COMMIT;

select * from knowledge_for_ticket;