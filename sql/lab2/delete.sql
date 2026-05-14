update tickets
set status_id = (select id from status where status_name = 'закрыт')
where title = 'Для удаления';

delete from tickets
where status_id = (select id from status where status_name = 'закрыт');