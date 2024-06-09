<script>
    let price = "Placeholder€";
    let stock = "Placeholder Name";
</script>

<style>
    .stock_info_div{
        grid-column: 1;
        width: 30%;
        padding-left: 50px;
        font-family: Arial, Helvetica, sans-serif;
    }
    .stock_name{
        grid-column: 2;
        grid-row: 1;
        padding-left: 20px;
        font-family: Arial, Helvetica, sans-serif;
    }
    .stock_info{
        grid-column: 2;
        grid-row: 3;
        border: gainsboro solid 2px;
        border-radius: 8px;
        padding-left: 20px;
        font-family: Arial, Helvetica, sans-serif;
    }
    p{
        color: grey;
        font-family: Arial, Helvetica, sans-serif;
    }
</style>

<main>
    <div class="stock_info_div">
        <div class = "stock_name">
            <h2>{stock}</h2>
        </div>
        <div class = "stock_info">
            <h3>Current Price</h3>
            <h2>{price}</h2>
            <p>Price at Market Close</p>
        </div>
    </div>
</main>