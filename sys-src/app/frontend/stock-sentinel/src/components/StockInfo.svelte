<script>
    let price = "$Placeholder";
    let stock = "Placeholder Name";
</script>

<style>
    .stock_info_div{
        grid-column: 1;
        width: 30%;

    }
    .stock_name{
        grid-column: 2;
        grid-row: 1;
    }
    .stock_info{
        grid-column: 2;
        grid-row: 3;
        border-style: solid;
    }
</style>

<main>
    <div class="stock_info_div">
        <div class = "stock_name">
            <h2>{stock}</h2>
        </div>
        <div class = "stock_info">
            <div> <h3> Current Price</h3> </div>
            <div> <h2>{price}</h2></div>
            <div> <p>Price at Market Close</p></div>
        </div>
    </div>
</main>
