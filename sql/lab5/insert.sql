INSERT INTO clients (client_name, client_age, email)
VALUES
    ('Иван Петров', 25, 'ivan@mail.com'),
    ('Анна Смирнова', 30, 'anna@mail.com');

INSERT INTO agents (agent_name, email)
VALUES
    ('Алексей Сидоров', 'alex@support.com'),
    ('Мария Иванова', 'maria@support.com');

INSERT INTO knowledge_base (title, knowledge_base_content)
VALUES
    ('Сброс пароля', 'Инструкция по сбросу пароля'),
    ('Ошибка входа', 'Решение проблемы авторизации');

INSERT INTO tickets (title, description, client_id, status)
VALUES
    ('Не работает вход', 'Не могу войти в систему', 1, 'открыт');