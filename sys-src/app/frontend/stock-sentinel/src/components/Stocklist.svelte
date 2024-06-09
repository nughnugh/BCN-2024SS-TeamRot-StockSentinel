<script>
    let stocks = ["Stock Name", "Stock Name", "Stock Name", "Stock Name", "Stock Name", "Stock Name", "Stock Name", "Stock Name"];
    let sentiments = [1, 1, 0, -1, 1, 0, -1, 0];
</script>

<style>
    .stock_info_div{
        width: 100%;
        padding-left: 50px;
        font-family: Arial, Helvetica, sans-serif;
    }
    .sources_table{
        border: gainsboro solid 2px;
        border-radius: 8px;
        padding-left: 20px;
        padding-right: 20px;
        font-family: Arial, Helvetica, sans-serif;
    }
    body{
        font-family: Arial, Helvetica, sans-serif;
    }
    th{
        font-weight: bold;
        color: darkgrey;
    }
    tr{
        border-bottom: 1px solid darkgrey;
    }
    td{
        padding: 10px;
    }
</style>

<main>
    <div class="stock_info_div">
        <h2>Stock Overview</h2>
        <table class="sources_table">
            <thead>
            <tr>
                <th>Stocks</th>
                <th>Sentiment</th>
            </tr>
            </thead>
            <tbody>
            {#each stocks as stock, i}
                <tr>
                    <td>{stock}</td>
                    <td>{sentiments[i]}</td>
                </tr>
            {/each}
            </tbody>
        </table>
    </div>
</main>