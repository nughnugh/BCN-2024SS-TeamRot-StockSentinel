const dotenv = require('dotenv');

dotenv.config({path: '../../.env'});

const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');
const app = express();
const port =  3000;

const pool = new Pool({
    user: process.env.POSTGRES_USER,
    password: process.env.POSTGRES_PASSWORD,
    host: process.env.PG_HOST,
    port: parseInt(process.env.PG_PORT),
    database: process.env.POSTGRES_DB
});

app.use(cors())

app.get('/api/sentiments',async (req, res) => {

    const query = `
        SELECT s.name,
               s.ticker_symbol,
               AVG(sn.sentiment) AS AVG_Sentiment
          FROM stock s, 
               stock_news sn
         WHERE s.stock_id = sn.stock_id
           AND sn.pub_date BETWEEN now() - INTERVAL '7 days' AND now()
        GROUP BY s.name , s.ticker_symbol;
    `;

    try {
        const result = await pool.query(query);
        res.status(200).json(result.rows);
    } catch (err) {
        console.error('Error executing query', err.stack);
        res.status(500);
    }
});

// GET like /api/stockData/(insert Stock name)
app.get('/api/StockDataFor/:stockName', async (req, res) => {
    const query = `
        SELECT sp.stock_price_val,
               sp.stock_price_time
          FROM stock s, 
               stock_price sp
         WHERE s.stock_id = sp.stock_id
           AND s.name = $1
    `;

    try {
        const result = await pool.query(query, [String(req.params.stockName),]);
        res.status(200).json(result.rows);
    } catch (err) {
        console.error('Error executing query', err.stack);
        res.status(500);
    }
});


// GET like /api/sentimentSources/(insert source name)/(insert stock name)
app.get('/api/sentimentSources/:stockName', async (req, res) => {
    const query = `
        SELECT s.ticker_symbol,
               s.name AS stock_name,
               sn.title,
               sn.sentiment,
               sn.url AS source
          FROM stock_news sn, 
               stock s
         WHERE s.name = $1
           AND sn.stock_id = s.stock_id
           AND sn.sentiment_exists;
    `

    try {
        const result = await pool.query(query, [String(req.params.stockName),]);
        res.status(200).json(result.rows);
    } catch (err) {
        console.error('Error executing query', err.stack);
        res.status(500);
    }
});

// GET like /api/SentimentDataFor/stockName=(insert Stock name)
app.get('/api/SentimentDataFor/:stockName', async (req, res) => {
    const query = `
        SELECT s.name,
               s.ticker_symbol,
               AVG(sn.sentiment) AS AVG_Sentiment
          FROM stock s,
               stock_news sn
         WHERE s.stock_id = sn.stock_id
           AND sn.pub_date BETWEEN now() - INTERVAL '7 days' AND now()
           AND s.name = $1
         GROUP BY s.ticker_symbol, s.name;
    `;

    try {
        const result = await pool.query(query, [String(req.params.stockName),]);
        res.status(200).json(result.rows);
    } catch (err) {
        console.error('Error executing query', err.stack);
        res.status(500);
    }
});

app.get('/api/historicalData/:stockName',async (req, res) => {

    // language=SQL format=false
const query = `
        with time_series as (
            SELECT DATE_TRUNC('day', a.n) as day
              FROM GENERATE_SERIES(
                      '2024-01-01'::timestamp,
                      DATE_TRUNC('day', now())::timestamp,
                      '1 day'::interval
                  ) as a(n)
            ),
            stock_sentiments as (
                SELECT DATE_TRUNC('day', stock_news.pub_date) as day,
                       AVG(stock_news.sentiment) as sentiment
                  FROM stock,
                       stock_news
                 WHERE stock.name = $1
                   AND stock_news.stock_id = stock.stock_id
                   AND stock_news.sentiment_exists
                 GROUP BY DATE_TRUNC('day', stock_news.pub_date)
            ),
            stock_prices as (
                SELECT DATE_TRUNC('day', stock_price.stock_price_time) as day,
                       AVG(stock_price.stock_price_val) as price
                  FROM stock,
                       stock_price
                 WHERE stock.name = $1
                   AND stock_price.stock_id = stock.stock_id
                GROUP BY DATE_TRUNC('day', stock_price.stock_price_time)
            )
            SELECT time_series.day, stock_sentiments.sentiment, stock_prices.price
            FROM time_series
            LEFT JOIN stock_sentiments on time_series.day = stock_sentiments.day
            LEFT JOIN stock_prices on time_series.day = stock_prices.day
            ;
        `

    try {
        const result = await pool.query(query, [String(req.params.stockName),]);
        res.status(200).json(result.rows);
    } catch (err) {
        console.error('Error executing query', err.stack);
        res.status(500);
    }
});

// GET like /api/ArticlesBySourceFor/(insert Stock name)
app.get('/api/historicalDataInRange/:stockName/:startDate/:endDate',async (req, res) => {
    let startDate = String(req.params.startDate);
    if(startDate === ""){
        startDate = '2024-01-01'
    }

    let endDate = String(req.params.endDate);

    if(startDate === ""){
        let today = new Date();
        let dd = String(today.getDate());

        let mm = String(today.getMonth()+1);
        let yyyy = String(today.getFullYear());
        if(dd<10)
        {
            dd='0'+dd;
        }

        if(mm<10)
        {
            mm='0'+mm;
        }
        startDate = mm+'-'+dd+'-'+yyyy;
    }

    // language=SQL format=false
    const query = `
        with time_series as (
            SELECT DATE_TRUNC('day', a.n) as day
              FROM GENERATE_SERIES(
                      $1::timestamp,
                      $2::timestamp,
                      '1 day'::interval
                  ) as a(n)
            ),
            stock_sentiments as (
                SELECT DATE_TRUNC('day', stock_news.pub_date) as day,
                       AVG(stock_news.sentiment) as sentiment
                  FROM stock,
                       stock_news
                 WHERE stock.name = $3
                   AND stock_news.stock_id = stock.stock_id
                   AND stock_news.sentiment_exists
                 GROUP BY DATE_TRUNC('day', stock_news.pub_date)
            ),
            stock_prices as (
                SELECT DATE_TRUNC('day', stock_price.stock_price_time) as day,
                       AVG(stock_price.stock_price_val) as price
                  FROM stock,
                       stock_price
                 WHERE stock.name = $3
                   AND stock_price.stock_id = stock.stock_id
                GROUP BY DATE_TRUNC('day', stock_price.stock_price_time)
            )
            SELECT time_series.day, stock_sentiments.sentiment, stock_prices.price
            FROM time_series
            LEFT JOIN stock_sentiments on time_series.day = stock_sentiments.day
            LEFT JOIN stock_prices on time_series.day = stock_prices.day
            ;
        `

    try {
        const result = await pool.query(query, [String(req.params.stockName),]);
        res.status(200).json(result.rows);
    } catch (err) {
        console.error('Error executing query', err.stack);
        res.status(500);
    }
});

app.listen(port, () => console.log(`Server started on port ${port}`));
app.use(cors({origin: 'http://localhost:8080'}))
