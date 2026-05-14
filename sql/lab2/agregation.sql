select s.status_name, count(*)
from tickets t
join status s on t.status_id = s.id
group by s.status_name
having count(*) > 1;

select s.status_name, avg(c.client_age) as avg_age
from tickets t
join status s on t.status_id = s.id
join clients c on t.client_id = c.id
group by s.status_name
order by avg_age;

select s.status_name, min(c.client_age) as min_age
from tickets t
join status s on t.status_id = s.id
join clients c on t.client_id = c.id
group by s.status_name
order by min_age;

select s.status_name, max(c.client_age) as max_age
from tickets t
join status s on t.status_id = s.id
join clients c on t.client_id = c.id
group by s.status_name
order by max_age;
