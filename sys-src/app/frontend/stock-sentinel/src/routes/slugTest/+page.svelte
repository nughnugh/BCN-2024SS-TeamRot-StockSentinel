<script lang="ts">
    export let data;
    import {onMount} from "svelte";

    let stocks: Stock[] = [];

    onMount(async function () {
        const response = await fetch("http://localhost:3000/api/sentiments");
        const data = await response.json();
        console.log(data);
        console.log("TEST");
        stocks = data;
    });
    interface Stock{
        name: string;
        ticker_symbol: string;
        avg_sentiment: string;
    }

</script>

<h1>Welcome to /slugTest! Here we Test the slugs</h1>

{#each data.items as choice}
    <div>
        <p>{choice.text}</p>
        <a href='/slugTest/{choice.name}'>{choice.name}</a>
    </div>
{/each}

{#each stocks as stock}
    <div>
        <p>{stock.name}</p>
        <a href='/slugTest/{stock.name}'>{stock.name}</a>
    </div>
{/each}

<style>
    h1, p{
        color: blue;
    }
    a{
        color: red;
    }
</style>