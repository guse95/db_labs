create or replace function is_agent_busy(p_agent_id integer)
returns boolean as $$
declare
    ticket_count integer;
begin
    select count(*) into ticket_count
    from public.tickets
    where agent_id = p_agent_id and status in ('открыт', 'в работе');

    return ticket_count >= 5;
end;
$$ language plpgsql;

create or replace procedure create_ticket_with_kb(
    p_title varchar,
    p_description text,
    p_client_id integer,
    p_kb_id integer
) as $$
begin
    insert into public.tickets (title, description, client_id, status)
    values (p_title, p_description, p_client_id, 'открыт');

    insert into public.knowledge_for_ticket (ticket_id, knowledge_id)
    values (currval(pg_get_serial_sequence('public.tickets', 'id')), p_kb_id);

exception
    when foreign_key_violation then
        raise notice 'Ошибка: Указанный клиент или статья базы знаний не существуют.';
    when others then
        raise notice 'Произошла непредвиденная ошибка при создании тикета.';
end;
$$ language plpgsql;

CREATE OR REPLACE FUNCTION close_ticket(ticket_id integer)
RETURNS void AS
$$
BEGIN
    UPDATE tickets
    SET status = 'закрыт'
    WHERE id = ticket_id;
END;
$$ LANGUAGE plpgsql;

