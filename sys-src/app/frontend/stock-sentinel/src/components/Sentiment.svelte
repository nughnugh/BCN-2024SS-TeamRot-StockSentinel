<script lang="ts">
     import {onMount} from "svelte";

     export let title:string;

     let stocks: Stock[] = [];

     onMount(async function () {
         const response = await fetch("http://localhost:3000/api/sentiments");
         const data = await response.json();
         console.log(data);
         stocks = data;
     });
     interface Stock{
         name: string;
         ticker_symbol: string;
         avg_sentiment: string;
     }

    function setSentimentColor(sentiment: string){
        if(Number(sentiment) > 0){
            return 'green';
        } else if (Number(sentiment)  < 0){
            return 'red';
        } else {
            return 'black';
        }
    }

    function setSentimentText(sentiment: string){
        if(Number(sentiment)  > 0){
            return 'Positive';
        } else if (Number(sentiment)  < 0){
            return 'Negative';
        } else {
            return 'Neutral;'
        }
    }
</script>

<style>
    .stock_info{
        border-radius: 8px;
        padding: 10px 20px;
        box-shadow: gainsboro 0 0 10px;
        border: 1px solid gainsboro;
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
    <div class = "stock_info">
        {#each stocks as stock}
            {#if stock.name === title }
                <h3>Current Sentiment</h3>
                <h2 style="color: {setSentimentColor(stock.avg_sentiment)}">{Math.round(Number(stock.avg_sentiment)*100)/ 100}</h2>
                <p>{setSentimentText(stock.avg_sentiment)}</p>
            {/if}
        {/each}

    </div>
</main>
