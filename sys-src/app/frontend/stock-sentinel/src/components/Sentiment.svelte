<script lang="ts">
     let sentiment:number = 1;

    function setSentimentColor(sentiment: number){
        if(sentiment > 0){
            return 'green';
        } else if (sentiment < 0){
            return 'red';
        } else {
            return 'black';
        }
    }
</script>

<style>
    .stock_info_div{
        grid-column: 2;
        width: 30%;
        padding-left: 50px;
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
    .space_maker{
        grid-column: 2;
        grid-row: 1;
        padding-left: 20px;
        color: white;
    }

</style>

<main>

    <div class="stock_info_div">
        <h2 class = "space_maker">ignore this</h2>
        <div class = "stock_info">
            <h3>Current Sentiment</h3>
            <h2 style="color: {setSentimentColor(sentiment)}">{sentiment}</h2>
            <p>Strongly Positive</p>
        </div>
    </div>

</main>
