create table results (
   result_id        serial primary key,
   event_id         int not null,
   athlete_id       int not null,
   performance_time float not null,
   age_category     varchar(50),
   foreign key ( event_id )
      references events ( event_id ),
   foreign key ( athlete_id )
      references athletes ( athlete_id )
);