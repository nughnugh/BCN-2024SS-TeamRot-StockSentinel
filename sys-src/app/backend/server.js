const express = require('express');
const { Pool } = require('pg');

const app = express();
const port =  3000;



const pool = new Pool({
    user: 'your_db_user', // Replace with DB user
    host: 'your_db_host', // Replace with DB host
    database: 'your_db_name', // Replace with DB name
    password: 'your_db_password', // Replace with DB password
    port: 5432,
});


app.get('/api/sentiments', async (req, res) => {
    const query =
    "SELECT"+
        "s.name AS stock_name," +
        "s.ticker_symbol,"+
        "sn.sentiment," +
    "FROM" +
        "stock s; "+
    "JOIN"+
        "stock_news sn ON s.stock_id = sn.stock_id;"
    ;

    try {
        const result = await pool.query(query);
        res.status(200).json(result.rows);
    } catch (err) {
        console.error('Error executing query', err.stack);
        res.status(500).json({ error: 'Internal server error' });
    }
});

app.get('/api/stockData', async (req, res) => {
    const query =
        "SELECT"+
            "s.name AS stock_name," +
            "s.ticker_symbol,"+
            "sp.stock_price_val," +
            "sp.stock_price_time"+
        "FROM" +
            "stock s"+
        "WHERE"+
            "stock_name =" + String(req.query("stockName")) + // GET like /api/stockData?stockName=(insert Stock name)
        "JOIN "+
            "stock_price sp ON s.stock_id = sp.stock_id;"
    ;

    try {
        const result = await pool.query(query);
        res.status(200).json(result.rows);
    } catch (err) {
        console.error('Error executing query', err.stack);
        res.status(500).json({ error: 'Internal server error' });
    }
});


// GET like /api/sentimentSources?sourceName=(insert source name)&?stockName=(insert stock name)
app.get('/api/sentimentSources', async (req, res) => {
    const query =
        "SELECT"+
            "sn.name AS source_name," +
            "s.ticker_symbol," +
            "s.name AS stock_name"+
        "FROM" +
            "stock_news sn"+
        "WHERE"+
            "source_name=" + String(req.query("sourceName")) +
            "AND" +
            "stock_name="+ String(req.query("stockName")) +
        "JOIN "+
            "stock s ON sn.stock_id = s.stock_id;"
    ;


    try {
        const result = await pool.query(query);
        res.status(200).json(result.rows);
    } catch (err) {
        console.error('Error executing query', err.stack);
        res.status(500).json({ error: 'Internal server error' });
    }
});

app.listen(port, () => console.log(`Server started on port ${port}`));
