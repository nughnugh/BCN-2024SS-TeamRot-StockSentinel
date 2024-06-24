const express = require('express');
const { Pool } = require('pg');

const app = express();
const port =  3000;

const pool = new Pool({
    user: 'st_user',
    host: 'localhost',
    database: 'postgres',
    password: '123',
    port: 5432,
});


app.get('/api/sentiments',async (req, res) => {

    const query =
        "SELECT "+
            " s.name,"+
            " AVG(sn.sentiment) as AVG_Sentiment "+
        " FROM "+
            " stock s, stock_news sn "+
        " WHERE s.stock_id = sn.stock_id AND EXTRACT('week' FROM sn.pub_date) = EXTRACT('week' FROM now()) "+
        " group by s.name; "

    try {
        const result = await pool.query(query);
        res.status(200).json(result.rows);
    } catch (err) {
        console.error('Error executing query', err.stack);
        res.status(500);
    }
});

// GET like /api/stockData?stockName=(insert Stock name)
app.get('/api/StockDataFor/:stockName', async (req, res) => {
    const query =
    "SELECT "+
        "s.name AS stock_name, "+
        "s.ticker_symbol, "+
        "sp.stock_price_val, "+
        "sp.stock_price_time "+
    "FROM "+
        "stock s, stock_price sp "+
    "WHERE "+
        "s.stock_id = sp.stock_id "+
        "AND EXTRACT('week' FROM sp.stock_price_time) = EXTRACT('week' FROM now()) "+
        "AND s.name = '" + String(req.params.stockName) + "';"
    ;

    try {
        const result = await pool.query(query);
        res.status(200).json(result.rows);
    } catch (err) {
        console.error('Error executing query', err.stack);
        res.status(500);
    }
});


// GET like /api/sentimentSources?sourceName=(insert source name)&?stockName=(insert stock name)
app.get('/api/sentimentSources/:stockName', async (req, res) => {
    const query =
    "SELECT "+
        "s.ticker_symbol, "+
        "s.name AS stock_name, "+
        "sn.title, "+
        "sn.sentiment, "+
        "sn.url "+
    "FROM "+
        "stock_news sn, stock s "+
    "WHERE "+
        "s.name = '" + String(req.params.stockName) + "' "+
        "AND  sn.stock_id = s.stock_id "+
        "AND sn.sentiment_exists ;"

    try {
        const result = await pool.query(query);
        res.status(200).json(result.rows);
    } catch (err) {
        console.error('Error executing query', err.stack);
        res.status(500);
    }
});

app.listen(port, () => console.log(`Server started on port ${port}`));
