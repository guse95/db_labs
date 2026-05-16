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
    CASE
        WHEN random() < 0.01
            THEN 'критическая ошибка сервера'
        ELSE 'обычный текст'
        END || i
from generate_series(1, 50000) s(i);

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
    'Ошибка в системе номер ' || i,
    floor(random() * 100000 + 1)::int,
    floor(random() * 1000 + 1)::int,
    (
     array[
         'открыт',
     'в работе',
     'решен',
     'закрыт'
         ]
        )[floor(random()*4 + 1)],
    now() - (random() * interval '365 days')
from generate_series(1, 1000000) s(i);