create database headhunter_vacancies;
create table employer
(
    id integer not null constraint employer_pk primary key,
    name text not null,
    employer_url text
);
create table experience
(
    id text not null constraint experience_pk primary key,
    name text not null
);
create table employment
(
    id text not null constraint employment_pk primary key,
    name text not null
);
create table vacancy
(
    id            integer not null
        constraint vacancy_pk
            primary key,
    name          text    not null,
    area          text    not null,
    city          text,
    salary_from   integer not null,
    salary_to     integer not null,
    vacancy_url   text,
    employer_id   integer
        constraint employer_fk
            references employer ("id"),
    employer_url  text,
    requirement   text,
    experience_id text
        constraint experience_fk
            references experience ("id"),
    employment    text
        constraint employment_fk
            references employment ("id")
);
create table area
(
    id   integer
        constraint area_id_pk
            primary key,
    name varchar(255)
);
alter table vacancy
    rename column area to area_id;

alter table vacancy
    alter column area_id type integer using area_id::integer;

alter table vacancy
    add constraint area_id_fk
        foreign key (area_id) references area;

alter table vacancy
    drop column city;

alter table vacancy
    drop column employer_url;
