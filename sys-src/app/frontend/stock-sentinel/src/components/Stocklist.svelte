<script lang="ts">
    import thumbsUp from '$lib/assets/thumbsUp.png';
    import thumbsDown from '$lib/assets/thumbsDown.png';
    import thumbNeutral from '$lib/assets/thumbNeutral.png';

    let stocks = [
        {name: 'Apple', ticker: 'AAPL', sentiment: 1},
        {name: 'Amazon', ticker: 'AMZN', sentiment: 1},
        {name: 'Tesla', ticker: 'TSL', sentiment: 0},
        {name: 'Random Stock', ticker: 'RST',sentiment: -1},
        {name: 'Microsoft', ticker: 'MIC',sentiment: 1},
        {name: 'Samsung', ticker: 'SMSG',sentiment: 0},
        {name: 'Another Stock', ticker: 'AST',sentiment: -1},
        {name: 'Last Stock', ticker: 'LAST',sentiment: 0}
    ]

    function chooseThumb(sentiment: number){
        if(sentiment > 0){
            return thumbsUp;
        } else if (sentiment < 0){
            return thumbsDown;
        } else {
            return thumbNeutral;
        }
    }

</script>

<style>
    .stock_info_div{
        display: flex;
        flex-direction: column;
    }

    .stock_table{
        border-collapse: collapse;
        border-radius: 8px;
        box-shadow: grey 0 0 10px;
    }

    th{
        font-weight: bold;
        color: darkgrey;
        padding: 10px 20px;
    }

    .table_title{
        font-weight: bold;
        color: black;
        text-align: left;
        font-size: large;
        padding-top: 20px;
    }

    .stocks{
        text-align: left;
        width: fit-content;
    }

    .ticker{
        text-align: center;
        width: auto;
    }

    .sentiment{
        text-align: right;
        width: 5%;
    }

    td{
        border-top: 1px solid gainsboro;
        padding: 10px 20px;
        margin-right:0;
        margin-left: 0;
    }

    td a {
        text-decoration: none;
        color: black;
        text-align: left;
    }

    td a:hover{
        text-decoration: underline;
    }

    tbody tr:hover{
        background: gainsboro;
        border-radius: 8px;
    }

    img{
        max-height: 20px;
        width: auto;
        padding-left: 10px;
    }
</style>

<main>
    <div class="stock_info_div">
        <h2>Stock Overview</h2>
        <table class="stock_table">
            <thead>
                <tr>
                    <th class = "table_title">Available Stocks</th>
                </tr>
                <tr>
                    <th class = "stocks">Stock Name</th>
                    <th class = "ticker">Ticker</th>
                    <th class = "sentiment">Sentiment</th>
                </tr>
            </thead>
            <tbody>
                {#each stocks as stock, i}
                    <tr>
                        <td class = "stocks" ><a href = "/dashboard">{stock.name}</a></td>
                        <td class = "ticker"><a href = "/dashboard">{stock.ticker}</a></td>
                        <td class = "sentiment">
                            {stock.sentiment}
                            <img src={chooseThumb(stock.sentiment)} alt = "thumb based on sentiment"/>
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
</main>