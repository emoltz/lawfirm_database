create table Cases
(
    case_id     integer primary key,
    topic       varchar(128),
    date_closed date                not null,
    paid        boolean,
    verdict     varchar(128),
    managed_by  varchar(128)  not null,
    presided_by integer             not null,
    foreign key (managed_by) references Lawyers (lid),
    foreign key (presided_by) references Judges (judgeid)
);

create table Clients
(
    cid       integer primary key,
    firstname char(32) not null,
    lastname  char(32) not null,
    email     varchar(128),
    phone     integer,
    unique (firstname, lastname, email)
);


create table part_of
(
    client_id integer not null,
    case_id   integer not null,
    primary key (client_id, case_id),
    foreign key (client_id) references Clients (cid),
    foreign key (case_id) references Cases (case_id)
);

create table Lawyers
(
    lid           integer primary key,
    firstname     char(32)         not null,
    lastname      char(32)         not null,
    title         char(128),
    email         varchar(128),
    unique (firstname, lastname, lid),
    specialty     char(128),
    rate_per_hour double precision not null
);

create table Documents_Forms
(
    did           integer primary key,
    title         char(128),
    external_link char(128),
    is_discovery  boolean
);

create table lawyers_file_docs
(
    date        date,
    lawyer      integer not null,
    doc_or_form integer not null,
    primary key (lawyer, doc_or_form),
    foreign key (lawyer) references Lawyers (lid),
    foreign key (doc_or_form) references Documents_Forms (did)
);

create table Judges
(
    court     char(180),
    judgeid   integer primary key,
    firstname varchar(128),
    lastname  varchar(128),
    primary key (firstname, lastname)

);

create table Paralegals
(
    pid              integer primary key,
    rate_per_hour    double precision not null,
    specialty        char(32),
    firstname        char(128)        not null,
    lastname         char(128)        not null,
    unique (firstname, lastname, pid),
    assigned_to_case integer,
    foreign key (assigned_to_case) references Cases (case_id)
);

create table Research
(
    rid      integer primary key,
    text     char(500),
    citation char(128)
);

create table Contacts_related_to
(
    cid              integer,
    id               integer,
    firstname        char(128),
    lastname         char(128),
    phone            integer,
    email            char(128),
    type_of_relation char(128),
    primary key (cid, id),
    foreign key (cid) references Clients (cid) on delete cascade
);

create table works_on
(
    case_id integer,
    lid     integer,
    hours   integer,
    primary key (case_id, lid),
    foreign key (lid) references Lawyers (lid),
    foreign key (case_id) references Cases (case_id)
);

create table associated_with
(
    case_id integer,
    rid     integer,
    did     integer,
    primary key (case_id, rid, did),
    foreign key (case_id) references Cases (case_id),
    foreign key (rid) references Research (rid),
    foreign key (did) references Documents_Forms (did)
);

