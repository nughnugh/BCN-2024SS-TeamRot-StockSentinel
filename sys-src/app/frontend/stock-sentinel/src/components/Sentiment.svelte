<script lang="ts">
     let sentiment:number = -1;

    function setSentimentColor(sentiment: number){
        if(sentiment > 0){
            return 'green';
        } else if (sentiment < 0){
            return 'red';
        } else {
            return 'black';
        }
    }

    function setSentimentText(sentiment:number){
        if(sentiment > 0){
            return 'Positive';
        } else if (sentiment < 0){
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
        <h3>Current Sentiment</h3>
        <h2 style="color: {setSentimentColor(sentiment)}">{sentiment}</h2>
        <p>{setSentimentText(sentiment)}</p>
    </div>
</main>
