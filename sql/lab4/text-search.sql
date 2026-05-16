drop index if exists idx_kb_trgm;

explain analyze
select *
from knowledge_base
where knowledge_base_content like '%ошибка%';

create extension if not exists pg_trgm;

create index idx_kb_trgm
    on knowledge_base
    using gin (knowledge_base_content gin_trgm_ops);

analyze tickets;

explain analyze
select *
from knowledge_base
where knowledge_base_content like '%ошибка%';

drop index if exists idx_kb_trgm;