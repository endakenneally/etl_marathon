create table events (
   event_id              serial primary key,
   event_name            varchar(255) not null,
   event_country         varchar(5) not null,
   event_start_date      date not null,
   event_end_date        date not null,
   event_distance_length float not null
);