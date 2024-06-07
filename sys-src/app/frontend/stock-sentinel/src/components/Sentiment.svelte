<script>
    let sentiment = "Placeholder";
</script>

<style>
    .sentiment_info_div{
        grid-row: 2;
        width: 30%;
        padding-left: 50px;
        border-style: solid;
    }


</style>

<main>
    <div class="sentiment_info_div">
        <div>
            <h2>Current Sentiment</h2>
        </div>
        <div>
            <div> <h3> Current Sentiment</h3> </div>
            <div> <h2 style="color: green">{sentiment}</h2></div>
            <div> <p>Strongly Positive</p></div>
        </div>
    </div>
</main>
