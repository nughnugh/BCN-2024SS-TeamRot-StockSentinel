<script>
    let sources = ["source1", "source2", "source3", "source4", "source5", "source6", "source7", "source8"];
    let articles = [1, 2, 3, 4, 5, 6, 7, 8];
    let sentiments = ["positive", "positive", "neutral", "negative" ,"positive" , "neutral", "negative", "positive"];
</script>

<style>
    .stock_info_div{
        width: 100%;
        padding-left: 50px;
        font-family: Arial, Helvetica, sans-serif;
    }
    .sources_table{
        grid-column: 2;
        grid-row: 1;
        border: gainsboro solid 2px;
        border-radius: 8px;
        padding-left: 20px;
        font-family: Arial, Helvetica, sans-serif;
    }
    th{
        font-weight: bold;
        color: darkgrey;
    }
    tr{
        border-bottom: 1px solid darkgrey;
    }
    td{
        padding: 10px;
    }
</style>

<main>
    <div class="stock_info_div">
        <table class="sources_table">
            <thead>
                <tr>
                    <th>Source</th>
                    <th>Articles</th>
                    <th>Sentiment</th>
                </tr>
            </thead>
            <tbody>
            {#each sources as source, i}
                <tr>
                    <td>{source}</td>
                    <td>{articles[i]}</td>
                    <td>{sentiments[i]}</td>
                </tr>
                {/each}
            </tbody>
        </table>
    </div>
</main>