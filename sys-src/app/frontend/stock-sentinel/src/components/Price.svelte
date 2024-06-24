<script>
    $: price = "$XX,XXX.XX";
</script>

<style>
    .price_info{
        border-radius: 8px;
        border: 1px solid gainsboro;
        padding: 10px 20px;
        box-shadow: gainsboro 0 0 10px;
    }

    h3, h2, p{
        padding-top: 5px;
        padding-bottom: 5px;
    }

    h3{
        font-weight: bold;
    }

    h2{
        font-size: larger;
        font-weight: bold;
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