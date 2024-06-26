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

app.use(cors());

app.get('/api/sentiments',async (req, res) => {

    const query =
        "SELECT "+
            " s.name,"+
            " s.ticker_symbol,"+
            " AVG(sn.sentiment) AS AVG_Sentiment "+
       " FROM "+
            " stock s, stock_news sn " +
       " WHERE s.stock_id = sn.stock_id AND sn.pub_date BETWEEN now() - INTERVAL '7 days' AND now() " +
       " GROUP BY s.name , s.ticker_symbol; "

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
    const query =
        "SELECT "+
           " sp.stock_price_val, "+
           " sp.stock_price_time "+
        " FROM "+
            "stock s, stock_price sp "+
        " WHERE "+
            "s.stock_id = sp.stock_id "+
        " AND s.name = '" + String(req.params.stockName) + "'"
    ;

    try {
        const result = await pool.query(query);
        res.status(200).json(result.rows);
    } catch (err) {
        console.error('Error executing query', err.stack);
        res.status(500);
    }
});


// GET like /api/sentimentSources/(insert source name)/(insert stock name)
app.get('/api/sentimentSources/:stockName', async (req, res) => {
    const query =
        "SELECT "+
            " s.ticker_symbol,"+
            " s.name AS stock_name,"+
            " sn.title,"+
            " sn.sentiment,"+
            " sn.url AS source "+
        " FROM "+
            " stock_news sn, stock s "+
        " WHERE "+
            " s.name = '" + String(req.params.stockName) + "' "+
            " AND  sn.stock_id = s.stock_id "+
            " AND sn.sentiment_exists; "


    try {
        const result = await pool.query(query);
        res.status(200).json(result.rows);
    } catch (err) {
        console.error('Error executing query', err.stack);
        res.status(500);
    }
});

// GET like /api/SentimentDataFor/stockName=(insert Stock name)
app.get('/api/SentimentDataFor/:stockName', async (req, res) => {
    const query =
        " SELECT "+
            " s.name, "+
            " s.ticker_symbol, "+
            " AVG(sn.sentiment) AS AVG_Sentiment "+
        " FROM "+
            " stock s, stock_news sn "+
        " WHERE s.stock_id = sn.stock_id AND sn.pub_date BETWEEN now() - INTERVAL '7 days' AND now() AND s.name = '" + String(req.params.stockName) + "' "+
        " GROUP BY s.ticker_symbol, s.name; "
    ;

    try {
        const result = await pool.query(query);
        res.status(200).json(result.rows);
    } catch (err) {
        console.error('Error executing query', err.stack);
        res.status(500);
    }
});

// GET like /api/ArticlesBySourceFor/(insert Stock name)
app.get('/api/ArticlesBySourceFor/:stockName', async (req, res) => {
    const query =
        "SELECT "+
            "s.ticker_symbol, "+
            "sn.source_url, " +
            "AVG(sn.sentiment) AS sentiment,"+
            "COUNT(sn.url) AS articles "+
        "FROM "+
            "stock_news sn, stock s "+
        "WHERE "+
            "s.name = '" + String(req.params.stockName) + "' "+
            "AND sn.sentiment_exists AND sn.pub_date BETWEEN now() - INTERVAL '7 days' AND now() " +
            "GROUP BY sn.source_url, s.ticker_symbol; "
    ;

    try {
        const result = await pool.query(query);
        res.status(200).json(result.rows);
    } catch (err) {
        console.error('Error executing query', err.stack);
        res.status(500);
    }
});

app.get('/api/historicalSentiments/:stockName',async (req, res) => {

    const query =
        "SELECT "+
        " s.name,"+
        " s.ticker_symbol," +
        "sn.pub_date, "+
        " AVG(sn.sentiment) AS AVG_Sentiment "+
        " FROM "+
        " stock s, stock_news sn " +
        " WHERE s.stock_id = sn.stock_id AND s.name = '" + String(req.params.stockName) + "' " +
        " GROUP BY s.name , s.ticker_symbol, sn.pub_date; "

    try {
        const result = await pool.query(query);
        res.status(200).json(result.rows);
    } catch (err) {
        console.error('Error executing query', err.stack);
        res.status(500);
    }
});

app.listen(port, () => console.log(`Server started on port ${port}`));
app.use(cors({origin: 'http://localhost:5173'}))
