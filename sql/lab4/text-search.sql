drop index if exists idx_trgm;

explain analyze
select *
from tickets
where description like '%ошибка%';

create extension if not exists pg_trgm;
create index idx_trgm
    on tickets
    using gin (description gin_trgm_ops);

analyze tickets;

explain analyze
select *
from tickets
where description like '%ошибка%';

drop index if exists idx_trgm;