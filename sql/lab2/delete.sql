update tickets
set status = 'закрыт'
where title = 'Для удаления';

delete from tickets
where status = 'закрыт';