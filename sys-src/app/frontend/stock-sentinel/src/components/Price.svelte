<script lang="ts">

    import {onMount} from "svelte";

    export let title:string;
    let prices: Price[] = [];

    onMount(async function () {
        const response = await fetch("http://localhost:3000/api/StockDataFor/"+ title);
        const params = await response.json();
        console.log(params);
        prices = params;
    });
    interface Price{
        stock_price_val: string;
        stock_price_time: string;
    }
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
        {#each prices as price, i}
            {#if i === 0}
                <h2>${price.stock_price_val}</h2>
            {/if}
        {/each}
        <p>Price at Market Close</p>
    </div>
</main>