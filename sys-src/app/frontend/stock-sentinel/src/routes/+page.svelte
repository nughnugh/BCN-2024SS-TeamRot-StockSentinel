<script>
    let price = "$ Placeholder $";
</script>

<style>
    .grid-container {
        display: grid;
        row-gap: 1px;
        column-gap: 5px;
    }
    .header{
        text-align: left;
        grid-row:1;
        grid-column: 1;
        border-style: solid;
    }
    .pages{
        text-align: left;
        grid-row:1;
        grid-column: 2;
    }
    .stock_name{
        grid-row:2;
        border-style: solid;
    }
    .stock_info{
        grid-row:3;
        border-style: solid;
    }
    .sentiment{
        grid-column: 2;
        border-style: solid;
    }
</style>

<div class="grid-container">
    <div class = "header"><h1> Stock Sentinel</h1> <div class="pages"> <h3>Overview</h3> </div></div>

    <div class="stock_name"> <h1>Stock Name</h1></div>
    <div class="stock_info">
        <h3>Current Price</h3>
        <h2>{price}</h2>
        <p> Price at Market Close</p>
    </div>
    <div class="sentiment"> <h3>Sentiment</h3> </div>
</div>

