insert into public.clients (client_name, email, client_age)
values
    ('Иван Иванов', 'ivan@example.com', 15),
    ('Денис Хлопов', 'denis@example.com', 24),
    ('Владимир Бондарев', 'vladimir@example.com', 47),
    ('Мария Петрова', 'maria@example.com', 32),
    ('Алексей Смирнов', 'alex@example.com', 29);

insert into public.agents (agent_name, email)
values
    ('Анна Support', 'anna@helpdesk.com'),
    ('Василиса Support', 'vasilisa@helpdesk.com'),
    ('Константин Support', 'konstantin@helpdesk.com'),
    ('Олег Support', 'oleg@helpdesk.com');

insert into public.status (status_name)
values
    ('открыт'),
    ('в работе'),
    ('решен'),
    ('закрыт');

insert into  public.knowledge_base (title, knowledge_base_content)
values
    ('Как восстановить пароль', 'Перейдите по ссылке "Забыли пароль" и следуйте инструкции'),
    ('Проблемы с оплатой', 'Проверьте баланс карты и повторите попытку'),
    ('Ошибка входа', 'Очистите кэш браузера и попробуйте снова');

insert into  public.tickets (title, description, client_id, agent_id, status_id)
values
    (
        'Не могу войти',
        'Система не принимает пароль',
        (select id from public.clients where email = 'ivan@example.com'),
        (select id from public.agents where email = 'vasilisa@helpdesk.com'),
        (select id from public.status where status_name = 'открыт')
    ),
    (
        'Ошибка оплаты',
        'Платеж не проходит',
        (select id from public.clients where email = 'maria@example.com'),
        (select id from public.agents where email = 'oleg@helpdesk.com'),
        (select id from public.status where status_name = 'в работе')
    ),
    (
        'Забыл пароль',
        'Как восстановить доступ?',
        (select id from public.clients where email = 'alex@example.com'),
        (select id from public.agents where email = 'anna@helpdesk.com'),
        (select id from public.status where status_name = 'решен')
    ),
    (
        'Забыл пароль',
        'Как восстановить доступ?',
        (select id from public.clients where email = 'maria@example.com'),
        (select id from public.agents where email = 'anna@helpdesk.com'),
        (select id from public.status where status_name = 'решен')
    ),
    (
        'Забыл пароль',
        'Как восстановить доступ?',
        (select id from public.clients where email = 'vladimir@example.com'),
        (select id from public.agents where email = 'anna@helpdesk.com'),
        (select id from public.status where status_name = 'решен')
    ),
    (
        'Проблемы с производительностью',
        'Компьютер выключается при запуске приложения',
        (select id from public.clients where email = 'vladimir@example.com'),
        (select id from public.agents where email = 'konstantin@helpdesk.com'),
        (select id from public.status where status_name = 'открыт')
    ),
    (
        'Бесконечная загрузка',
        'При нажатии на ктнопку приложении грузится и ничего не происходит',
        (select id from public.clients where email = 'ivan@example.com'),
        (select id from public.agents where email = 'anna@helpdesk.com'),
        (select id from public.status where status_name = 'в работе')
    ),
    (
        'Для удаления',
        'Неважно',
        (select id from public.clients where email = 'denis@example.com'),
        (select id from public.agents where email = 'anna@helpdesk.com'),
        (select id from public.status where status_name = 'решен')
    );