delete from entries;

insert into entries(date, title, content) values (now() - interval '10 days', 'ЖК West Towers', 'Ужгород, вул. Легоцького, 64а, 64б');
insert into entries(date, title, content) values (now() - interval '1 day', 'ЖК Central Park Vinnytsia', 'Вінниця, вул. Цегельна, 12');
insert into entries(title, content) values ('ЖК Panorama de Luxe', 'Рівне, вул. Чорновола Вячеслава, 94 В, Д');