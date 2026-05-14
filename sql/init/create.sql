create table public.clients (
    id uuid default gen_random_uuid() not null,
    client_name varchar(100) null,
    client_age int not null check(client_age < 100 and client_age > 3),
    email varchar(255) not null,
    constraint clients_pk primary key (id),
    constraint clients_unique unique (email)
);

create table public.agents (
    id uuid default gen_random_uuid() not null,
    agent_name varchar(100) null,
    email varchar(255) not null,
    constraint agents_pk primary key (id),
    constraint agents_unique unique (email)
);

create table public.knowledge_base (
    id uuid default gen_random_uuid() not null,
    title varchar(255) null,
    knowledge_base_content text null,
    created_at timestamp default CURRENT_TIMESTAMP null,
    constraint knowledge_base_pkey primary key (id)
);

create table public.status (
    id uuid default gen_random_uuid() not null,
    status_name varchar(10) not null check(status_name in ('открыт', 'в работе', 'решен', 'закрыт')),
    constraint ticket_status_pk primary key (id),
    constraint ticket_status_unique unique (status_name)
);

create table public.tickets (
    id uuid default gen_random_uuid() not null,
    title varchar(255) null,
    description text null,
    client_id uuid not null,
    agent_id uuid null,
    status_id uuid not null,
    created_at timestamp default now() not null,
    constraint tickets_pk primary key(id),

    constraint tickets_agents_fk foreign key(agent_id) references public.agents(id),
    constraint tickets_clients_fk foreign key(client_id) references public.clients(id),
    constraint tickets_ticket_status_fk foreign key(status_id) references public.status(id)
);


