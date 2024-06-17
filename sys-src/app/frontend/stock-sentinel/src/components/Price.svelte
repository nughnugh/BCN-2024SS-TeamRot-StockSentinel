<script>
    let price = "$XX,XXX.XX";
</script>

<style>
    .price_info{
        border: gainsboro solid 2px;
        border-radius: 8px;
        padding-left: 20px;
        box-shadow: gainsboro 0px 0px 10px;
    }

    p{
        color: grey;
    }
</style>

<main>
    <div class = "price_info">
        <h3>Current Price</h3>
        <h2>{price}</h2>
        <p>Price at Market Close</p>
    </div>
</main>