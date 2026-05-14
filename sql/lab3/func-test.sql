call create_ticket_with_kb(
    'Проблема с сетью',
    'Не работает Wi-Fi',
    9999,
    1
);

select agent_name, is_agent_busy(id) as busy_status
from public.agents;

insert into public.clients (client_name, client_age, email)
values ('Малыш', 5, 'baby@example.com');