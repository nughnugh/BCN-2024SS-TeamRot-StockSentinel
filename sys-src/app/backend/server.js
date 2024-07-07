import dotenv from 'dotenv';
import dateFormat from 'dateformat';
import pg from 'pg';
import cors from 'cors';
import express from 'express';

dotenv.config({path: '../../.env'});

const app = express();
const port =  3000;

const pool = new pg.Pool({
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
        GROUP BY s.name , s.ticker_symbol
        ORDER BY AVG_Sentiment DESC;
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
        SELECT sp.stock_price_val
          FROM stock s, 
               stock_price sp
         WHERE s.stock_id = sp.stock_id
           AND s.name = $1
         ORDER BY sp.stock_price_time DESC
         LIMIT 1
    `;

    try {
        const result = await pool.query(query, [String(req.params.stockName),]);
        res.status(200).json(result.rows[0]);
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
app.get('/api/ArticlesBySourceFor/:stockName', async (req, res) => {
    const query = `
        SELECT
            ns.url AS source_url,
            TRUE AS visible,
            AVG(sn.sentiment) AS sentiment,
            COUNT(sn.url) AS articles
        FROM news_source ns,
             stock_news sn,
             stock s
        WHERE s.name = $1
            AND s.stock_id = sn.stock_id
            AND ns.news_source_id = sn.news_source_id
            AND sn.sentiment_exists
        GROUP BY ns.url
        ORDER BY articles DESC
    `;

    try {
        const result = await pool.query(query, [String(req.params.stockName),]);
        res.status(200).json(result.rows);
    } catch (err) {
        console.error('Error executing query', err.stack);
        res.status(500);
    }
});

app.get('/api/historicalDataInRange',async (req, res) => {
    let oneYearFromNow = new Date();
    oneYearFromNow.setFullYear(oneYearFromNow.getFullYear() - 1);

    let startDate = req.query.startDate || '2024-01-01'; //dateFormat(oneYearFromNow, 'yyyy-mm-dd');
    let endDate = req.query.endDate || dateFormat(Date.now(), 'yyyy-mm-dd');
    let stockName = String(req.query.stockName);
    let groupingTime = req.query.groupingTime || 1;
    let excludedSources = [];
    if(req.query.excludedSources) {
        try {
            excludedSources = JSON.parse(req.query.excludedSources);
        } catch (err) {
            console.error('Error parsing excluded sources:', err.stack);
        }
    }

    const query = `
        with time_series as (
            SELECT DATE_TRUNC('day', a.n) as day
              FROM GENERATE_SERIES(
                      $3::timestamp,
                      $4::timestamp,
                      '1 day'::interval
                  ) as a(n)
        ),
        stock_sentiment_pre as (
            SELECT (EXTRACT('year' FROM stock_news.pub_date) || '-01-01')::date
                   + interval '1' day * (FLOOR(EXTRACT('doy' FROM stock_news.pub_date) / $2) * $2 + floor($2 / 2)) as day,
                   stock_news.sentiment as sentiment
              FROM stock,
                   stock_news,
                   news_source,
                   time_series
             WHERE stock.name = $1
               AND stock_news.stock_id = stock.stock_id
               AND stock_news.news_source_id = news_source.news_source_id
               AND NOT (news_source.url = ANY($5))
               AND stock_news.sentiment_exists
               AND DATE_TRUNC('day', stock_news.pub_date) = time_series.day
            order by stock_news.pub_date
        ),
        stock_sentiments as (
            SELECT stock_sentiment_pre.day,
                   avg(stock_sentiment_pre.sentiment) as sentiment
              FROM stock_sentiment_pre
            GROUP BY stock_sentiment_pre.day
        ),
        stock_prices as (
            SELECT DATE_TRUNC('day', stock_price.stock_price_time) as day,
                   AVG(stock_price.stock_price_val) as price
              FROM stock,
                   stock_price,
                   time_series
             WHERE stock.name = $1
               AND stock_price.stock_id = stock.stock_id
               AND stock_price.stock_price_time = time_series.day
            GROUP BY stock_price.stock_price_time
        )
        SELECT time_series.day, stock_sentiments.sentiment, stock_prices.price
        FROM time_series
        LEFT JOIN stock_sentiments on time_series.day = stock_sentiments.day
        LEFT JOIN stock_prices on time_series.day = stock_prices.day;
    `;

    try {
        const result = await pool.query(query, [stockName, groupingTime, startDate, endDate, excludedSources]);
        res.status(200).json(result.rows);
    } catch (err) {
        console.error('Error executing query', err.stack);
        res.status(500);
    }
});

app.listen(port, () => console.log(`Server started on port ${port}`));
app.use(cors({origin: 'http://localhost:8080'}))
