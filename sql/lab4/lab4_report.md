# Лабораторная работа №4

# Используемая база данных

В работе использовалась база данных системы технической поддержки,
содержащая следующие таблицы:

* `clients`
* `agents`
* `tickets`
* `knowledge_base`
* `knowledge_for_ticket`


# Объем данных

В ходе лабораторной работы база данных была заполнена тестовыми данными:

| Таблица        | Количество строк |
| -------------- |------------------|
| clients        | 100 000          |
| agents         | 1 000            |
| knowledge_base | 50 000           |
| tickets        | 1 000 000        |

# Исследуемые сценарии

## 1. Сложный фильтр

## SQL запрос

```sql
select *
from tickets
where status = 'открыт'
  and created_at > now() - interval '30 days';
```

## Гипотеза

Составной индекс `(status, created_at)` должен ускорить выполнение запроса, 
так как запрос содержит:

* точное сравнение,
* диапазонное условие.

## План выполнения без индекса

```text
Parallel Seq Scan
Execution Time: 46.508 ms
```

PostgreSQL выполнил последовательное сканирование таблицы.

## Индекс

```sql
create index idx_tickets_status_created on tickets(status, created_at);
```

## План выполнения после индекса

```text
Bitmap Heap Scan
Bitmap Index Scan on idx_tickets_status_created
Execution Time: 0.054 ms
```

## Результат

| Без индекса | С индексом |
| ----------- |------------|
| 46.508 ms   | 0.054 ms   |

## Вывод

Составной индекс значительно ускорил выполнение запроса.
PostgreSQL заменил `Seq Scan` на `Bitmap Index Scan`, 
что позволило сократить количество просматриваемых строк.

## 2. ORDER BY и LIMIT

## SQL запрос

```sql
select *
from tickets
order by created_at desc
    limit 100;
```

## Гипотеза

Индекс по `created_at` должен ускорить сортировку и выборку первых строк.

## План выполнения без индекса

```text
Parallel Seq Scan
Sort Method: top-N heapsort
Execution Time: 50.263 ms
```

PostgreSQL выполнил полное сканирование таблицы с последующей сортировкой.

## Индекс

```sql
create index idx_tickets_created_at on tickets(created_at desc);
```

## План выполнения после индекса

```text
Parallel Seq Scan
Execution Time: 0.191 ms
```

## Результат

| Без индекса | С индексом |
| ----------- |------------|
| 50.263 ms   | 0.191 ms   |

## Вывод

Создание индекса позволило сократить время выполнения запроса. 
Однако PostgreSQL продолжил использовать последовательное сканирование таблицы, 
поскольку выборка затрагивала большое количество строк.

## 3. Альтернативные варианты индексирования

## SQL запрос

```sql
select *
from tickets
where agent_id = 10
  and status = 'в работе';
```

## Гипотеза

Составной индекс `(agent_id, status)` должен работать эффективнее одиночного индекса `(agent_id)`.

## План выполнения без индекса

```text
Parallel Seq Scan
Execution Time: 31.586 ms
```

## Индекс

```sql
create index idx_agent on tickets(agent_id);
```

## План выполнения с индексом `idx_agent`

```text
Bitmap Heap Scan
Bitmap Index Scan on idx_agent
Execution Time: 1.596 ms
```

## Индекс

```sql
create index idx_agent_status on tickets(agent_id, status);
```

## План выполнения с индексом `idx_agent_status`

```text
Bitmap Heap Scan
Bitmap Index Scan on idx_agent_status
Execution Time: 0.047 ms
```

## Результат

| Вариант          | Время     |
| ---------------- | --------- |
| Без индекса      | 31.586 ms |
| idx_agent        | 1.596 ms  |
| idx_agent_status | 0.047 ms  |

## Вывод

Составной индекс оказался наиболее эффективным,
поскольку PostgreSQL смог выполнять поиск сразу по двум условиям 
без дополнительной фильтрации строк.

## 4. Текстовый поиск

## SQL запрос

```sql
select *
from tickets
where description like '%ошибка%';
```

## Гипотеза

GIN-индекс с расширением `pg_trgm` должен ускорить поиск подстроки.

## План выполнения без индекса

```text
Parallel Seq Scan
Execution Time: 57.540 ms
```

## Индекс

```sql
create extension if not exists pg_trgm;
create index idx_trgm on tickets
    using gin (description gin_trgm_ops);
```

## План выполнения после индекса

```text
Bitmap Heap Scan
Bitmap Index Scan on idx_trgm
Execution Time: 21.421 ms
```

## Результат

| Без индекса | С индексом  |
| ----------- |-------------|
| 57.540 ms   | 21.421 ms   |

## Вывод

GIN-индекс значительно ускорил выполнение текстового поиска.
PostgreSQL перестал выполнять полное сканирование таблицы и 
начал использовать индексный поиск с разбиением на триграммы.

## 5. JOIN-запрос

## SQL запрос

```sql
select
    t.id,
    c.client_name,
    a.agent_name
from tickets t
         join clients c on c.id = t.client_id
         join agents a on a.id = t.agent_id
where t.status = 'решен';
```

## Гипотеза

Индексы по полям `client_id`, `agent_id` и `status` должны ускорить выполнение JOIN-запроса.

## План выполнения без индексов

```text
Hash Join
Seq Scan on tickets
Seq Scan on clients
Seq Scan on agents
Execution Time: 175.493 ms
```

## Индексы

```sql
create index idx_tickets_client on tickets(client_id);

create index idx_tickets_agent on tickets(agent_id);

create index idx_tickets_status on tickets(status);
```

## План выполнения после индексов

```text
Hash Join
Bitmap Heap Scan
Bitmap Index Scan on idx_tickets_status
Seq Scan on clients
Seq Scan on agents
Execution Time: 154.700 ms
```

## Результат

| Без индекса | С индексом |
| ----------- | ---------- |
| 175.493 ms  | 154.700 ms |

## Вывод

Индексы дали незначительное ускорение JOIN-запроса. PostgreSQL продолжил использовать стратегию `Hash Join`, 
поскольку условие `status = 'решен'` возвращало достаточно большое количество строк: `189991`, 
и последовательное чтение таблиц оставалось более выгодным для оптимизатора.

## 6. Негативный сценарий

## SQL запрос

```sql
select *
from tickets
where status != 'закрыт';
```

## Гипотеза

Индекс по `status` не будет использоваться, поскольку запрос возвращает большую часть таблицы.

## План выполнения без индекса

```text
Seq Scan
Execution Time: 96.305 ms
```

## Индекс   

```sql
create index idx_tickets_status on tickets(status);
```

## План выполнения после индекса

```text
Seq Scan
Execution Time: 103.970 ms
```

## Результат

| Без индекса | С индексом |
|-------------| ---------- |
| 96.305 ms   | 103.970 ms |

## Вывод

PostgreSQL полностью проигнорировал индекс и продолжил использовать `Seq Scan`. 
Это связано с низкой селективностью условия: `800099`.

## Исследование влияния индексов на INSERT/UPDATE

## SQL запрос

### Insert
```sql
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
```

### Update
```sql
update tickets
set status = 'закрыт'
where status = 'открыт';
```

## Гипотеза

При наличии большого количества индексов операции вставки и обновления данных выполняются медленнее, 
поскольку PostgreSQL вынужден дополнительно обновлять индексные структуры.

## План выполнения без индекса для insert

```text
Seq Scan
Execution Time: 21330.332 ms
```

## Индексы

```sql
create index idx_tickets_status on tickets(status);

create index idx_tickets_agent on tickets(agent_id);

create index idx_tickets_created_at on tickets(created_at);
```

## План выполнения после индекса для insert

```text
Seq Scan
Execution Time: 58631.763 ms
```

## План выполнения без индекса для update

```text
Seq Scan
Execution Time: 95.755 ms
```

## Индекс

```sql
create index idx_tickets_status on tickets(status);
```

## План выполнения после индекса для update

```text
Seq Scan
Execution Time: 40891.644 ms
```

## Результат

| операция\индекс | Без индекса  | С индексом   |
|-----------------|--------------|--------------|
| insert          | 21330.332 ms | 58631.763 ms |
| update          | 95.755 ms    | 40891.644 ms |

## Вывод

Наличие индексов значительно замедлило операции `INSERT` и `UPDATE`. 
Это связано с тем, что PostgreSQL при изменении данных дополнительно обновляет 
все связанные индексные структуры, что особенно заметно при обработке большого количества строк.


# Общий вывод

В ходе лабораторной работы было установлено, 
что индексы существенно ускоряют выполнение селективных запросов, особенно в случаях, 
когда условия отбора возвращают небольшую часть данных таблицы. Также было показано, 
что составные индексы являются более эффективными при фильтрации по нескольким полям одновременно, 
так как позволяют уменьшить количество проверяемых строк уже на уровне индексного поиска. 
Для задач текстового поиска улучшенные результаты демонстрируют GIN-индексы, 
которые в сочетании с расширением pg_trgm обеспечивают значительное ускорение поиска по подстрокам.

При этом было выявлено, что индексы не всегда приводят к улучшению производительности запросов. 
В случаях низкой селективности условий PostgreSQL предпочитает последовательное сканирование таблицы (Seq Scan), 
поскольку оно оказывается дешевле, чем использование индекса. 
Аналогично, в JOIN-запросах оптимизатор может выбирать стратегию Hash Join, даже при наличии индексов, 
если это обеспечивает более эффективное выполнение запроса на больших объёмах данных.

Эксперимент показал, что эффективность индекса зависит от:
* структуры запроса;
* распределения данных;
* количества возвращаемых строк;
* селективности условий.
