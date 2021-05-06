create table if not exists zipcodes (
    id int auto_increment not null,
    zipcode varchar(5) not null,
    primary key(id)
);

create table if not exists surgeons (
    id int auto_increment not null,
    title varchar(255) null,
    phone varchar(255) null,
    training text null,
    latlng varchar(255) null,
    locations JSON null,
    languages text null,
    zipcode varchar(255) null,
    primary key (id)
);

create table if not exists valid_zipcodes (
    id int auto_increment not null,
    zipcode varchar(5) not null,
    primary key (id)
);
