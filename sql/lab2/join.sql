select * from clients c
right join tickets t on c.id = t.client_id;

select * from agents a
left join tickets t on a.id = t.agent_id;