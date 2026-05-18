insert into clients (client_name, client_age, email)
select
    'Client_' || i,
    floor(random() * 60 + 18)::int,
    'client' || i || '@mail.com'
from generate_series(1, 100000) s(i);

insert into agents (agent_name, email)
select
    'Agent_' || i,
    'agent' || i || '@company.com'
from generate_series(1, 1000) s(i);

insert into knowledge_base(title, knowledge_base_content)
select
    'Article ' || i,
    'ошибка сервера' || i
from generate_series(1, 50000) s(i);

drop index if exists idx_tickets_status;
drop index if exists idx_tickets_agent;
drop index if exists idx_tickets_created_at;

explain analyze
insert into tickets (
    title,
    description,
    client_id,
    agent_id,
    status,
    created_at
)
select
    'Ticket #' || i,
    CASE
        WHEN random() < 0.01
        THEN 'критическая ошибка сервера'
        ELSE 'обычный текст'
    END || i,
    floor(random() * 100000 + 1)::int,
    floor(random() * 1000 + 1)::int,
    CASE
        WHEN random() < 0.80 THEN 'закрыт'
        WHEN random() < 0.95 THEN 'решен'
        WHEN random() < 0.99 THEN 'в работе'
        ELSE 'открыт'
    END,
    now() - (random() * interval '365 days')
from generate_series(1, 500000) s(i);

create index idx_tickets_status on tickets(status);
create index idx_tickets_agent on tickets(agent_id);
create index idx_tickets_created_at on tickets(created_at);

analyze tickets;

explain analyze
insert into tickets (
    title,
    description,
    client_id,
    agent_id,
    status,
    created_at
)
select
    'Ticket #' || i,
    CASE
        WHEN random() < 0.01
        THEN 'критическая ошибка сервера'
        ELSE 'обычный текст'
    END || i,
    floor(random() * 100000 + 1)::int,
    floor(random() * 1000 + 1)::int,
    CASE
        WHEN random() < 0.80 THEN 'закрыт'
        WHEN random() < 0.95 THEN 'решен'
        WHEN random() < 0.99 THEN 'в работе'
        ELSE 'открыт'
    END,
    now() - (random() * interval '365 days')
from generate_series(500001, 1000000) s(i);

drop index if exists idx_tickets_status;
drop index if exists idx_tickets_agent;
drop index if exists idx_tickets_created_at;