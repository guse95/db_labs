create or replace view ticket_info as
select
    t.id,
    t.title,
    c.client_name,
    c.client_age,
    s.status_name
from tickets t
         join clients c on t.client_id = c.id
         join status s on t.status_id = s.id;

create or replace view agent_ticket_stats as
select
    a.agent_name,
    count(t.id) as ticket_count
from agents a
         left join tickets t on a.id = t.agent_id
group by a.agent_name;

create or replace view unassigned_tickets as
select
    t.id,
    t.title,
    c.client_name,
    s.status_name,
    t.created_at
from tickets t
join clients c on t.client_id = c.id
join status s on t.status_id = s.id
where status_name = 'открыт';

select * from ticket_info
order by client_age;

select * from ticket_info
where status_name = 'решен'
order by title;

select * from agent_ticket_stats
order by ticket_count desc;

select * from unassigned_tickets
order by created_at