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
    stock_price_id   bigserial,
    stock_id         serial
        constraint stock_price_stock_stock_id_fk
            references stock,
    stock_price_time timestamptz not null,
    stock_price_val  numeric   not null,
    primary key(stock_id, stock_price_time)
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
    stock_news_id    bigserial,
    stock_id         serial
        constraint stock_news_stock_stock_id_fk
            references stock,
    news_source_id   integer
        constraint stock_news_news_source_news_source_id_fk
            references news_source,
    url              TEXT,
    sentiment_exists boolean default false not null,
    sentiment        numeric,
    ticker_related   boolean,
    pub_date         timestamptz NOT NULL,
    title            TEXT,
    timeout_cnt      integer default 0     not null,
	primary key(stock_news_id, pub_date)
);

alter table stock_news
    owner to st_user;

CREATE INDEX ON stock_news (stock_id, pub_date DESC);
CREATE INDEX ON stock_price (stock_id, stock_price_time DESC);
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
SELECT create_hypertable('stock_price', by_range('stock_price_time'));
SELECT create_hypertable('stock_news', by_range('pub_date'));
