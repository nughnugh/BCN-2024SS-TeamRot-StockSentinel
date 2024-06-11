create table stock
(
    stock_id      serial
        constraint stock_pk
            primary key,
    name          varchar(20) not null,
    ticker_symbol varchar(5)  not null
        constraint stock_ak
            unique
);

alter table stock
    owner to st_user;

create table stock_price
(
    stock_price_id   bigserial
        constraint stock_price_pk
            primary key,
    stock_id         serial
        constraint stock_price_stock_stock_id_fk
            references stock,
    stock_price_time timestamp not null,
    stock_price_val  numeric   not null,
    constraint stock_price_pk_2
        unique (stock_price_time, stock_id)
);

alter table stock_price
    owner to st_user;

create table news_source
(
    news_source_id serial
        constraint news_source_pk
            primary key,
    name           varchar(64) not null,
    url            varchar(128)
        constraint news_source_pk_2
            unique
);

alter table news_source
    owner to st_user;

create table stock_news
(
    stock_news_id    bigserial
        constraint stock_news_pk
            primary key,
    stock_id         serial
        constraint stock_news_stock_stock_id_fk
            references stock,
    news_source_id   integer
        constraint stock_news_news_source_news_source_id_fk
            references news_source,
    url              varchar(256)
        constraint stock_news_pk_2
            unique,
    sentiment_exists boolean default false not null,
    sentiment_neg    numeric,
    sentiment_neu    numeric,
    sentiment_pos    numeric,
    sentiment_comp   numeric,
    ticker_related   boolean,
    pub_date         timestamp,
    timeout          boolean default false not null,
    title            varchar(256)
);

alter table stock_news
    owner to st_user;

