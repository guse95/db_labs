select t.status, count(*)
from tickets t
group by t.status
having count(*) > 1;

select t.status, avg(c.client_age) as avg_age
from tickets t
join clients c on t.client_id = c.id
group by t.status
order by avg_age;

select t.status,
       min(c.client_age) as min_age,
       max(c.client_age) as max_age
from tickets t
         join clients c on t.client_id = c.id
group by t.status
order by min_age;
