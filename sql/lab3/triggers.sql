create or replace function check_client_before_insert()
returns trigger as $$
begin
    if new.client_age == null then
        raise exception 'Введите возраст.';
    end if;
    if new.client_age < 0 then
        raise exception 'Невалидный возраст для клиента %. Возраст не может быть ниже нуля.', new.client_name;
    end if;
    if new.client_age < 18 then
        raise exception 'Клиент % слишком молод. Регистрация доступна только с 18 лет.', new.client_name;
    end if;
    return new;
end;
$$ language plpgsql;

create trigger trg_check_client_age_insert
    before insert on public.clients
    for each row execute function check_client_before_insert();

create trigger trg_check_client_age_update
    before update on public.clients
    for each row execute function check_client_before_insert();


create or replace function log_ticket_status_change()
returns trigger as $$
begin
    if old.status <> new.status then
        raise notice 'Статус тикета №% изменен с % на %', new.id, old.status, new.status;
end if;
return new;
end;
$$ language plpgsql;

create trigger trg_ticket_status_notify
    after update on public.tickets
    for each row execute function log_ticket_status_change();