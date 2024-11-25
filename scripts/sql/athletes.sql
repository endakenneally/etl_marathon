create table athletes (
   athlete_id      serial primary key,
   athlete_name    varchar(255) not null,
   athlete_country varchar(5) not null,
   year_of_birth   int,
   gender          char(1) not null,
   club            varchar(255)
);