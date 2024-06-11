<script lang="ts">
    import thumbsUp from '$lib/assets/thumbsUp.png';
    import thumbsDown from '$lib/assets/thumbsDown.png';
    import thumbNeutral from '$lib/assets/thumbNeutral.png';

    let stocks = ["Stock Name 1", "Stock Name 2", "Stock Name 3", "Stock Name 4", "Stock Name 5", "Stock Name 6", "Stock Name 7", "Stock Name 8"];
    let sentiments = [1, 1, 0, -1, 1, 0, -1, 0];

    function chooseThumb(sentiment: number){
        if(sentiment > 0){
            return thumbsUp;
        } else if (sentiment < 0){
            return thumbsDown;
        } else {
            return thumbNeutral;
        }
    }
</script>

<style>
    .stock_info_div{
        display: flex;
        flex-direction: column;
    }

    .stock_table{
        border: gainsboro solid 2px;
        border-radius: 8px;
        padding-left: 20px;
        padding-right: 20px;
        box-shadow: gainsboro 0px 0px 10px;
    }

    th{
        font-weight: bold;
        color: darkgrey;
        padding-bottom: 10px;
    }

    .table_title{
        font-weight: bold;
        color: black;
        text-align: left;
        font-size: large;
        padding-top: 10px;
    }

    .stock_headline{
        text-align: left;
    }

    .sentiment_headline{
        text-align: right;
    }

    td{
        border-top: 1px solid gainsboro;
        padding-top: 10px;
        padding-bottom: 10px;
    }

    .stock_names{
        text-align: left;
    }

    .sentiment{
        text-align: right;
    }

    td a {
        text-decoration: none;
        color: black;
    }

    img{
        max-height: 20px;
        width: auto;
        padding-left: 10px;
    }
</style>

<main>
    <div class="stock_info_div">
        <h2>Stock Overview</h2>
        <table class="stock_table">
            <thead>
                <tr>
                    <th class = "table_title">Available Stocks</th>
                </tr>
                <tr>
                    <th class = "stock_headline">Stock Name</th>
                    <th class = "sentiment_headline">Sentiment</th>
                </tr>
            </thead>
            <tbody>
                {#each stocks as stock, i}
                    <tr>
                        <td class = "stock_names"><a href = "/dashboard">{stock}</a></td>
                        <td class = "sentiment">
                            {sentiments[i]}
                            <img src={chooseThumb(sentiments[i])} alt = "thumb based on sentiment"/>
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
</main>