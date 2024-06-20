<script lang="ts">
    import show from '$lib/assets/show.png';
    import hide from '$lib/assets/hide.png';

    let stocks = [
        {name: 'source1', articles: 1, sentiment: 'positive', visible: true},
        {name: 'source2', articles: 2, sentiment: 'positive', visible: true},
        {name: 'source3', articles: 3, sentiment: 'neutral', visible: true},
        {name: 'source4', articles: 4, sentiment: 'negative', visible: true},
        {name: 'source5', articles: 5, sentiment: 'positive', visible: true},
        {name: 'source6', articles: 6, sentiment: 'neutral', visible: true},
        {name: 'source7', articles: 7, sentiment: 'negative', visible: true},
        {name: 'source8', articles: 8, sentiment: 'positive', visible: true},
    ]

    function toggleVisibility(index: number){
        stocks[index].visible = !stocks[index].visible;
    }
</script>

<style>
    .stock_info_div{
        display:flex;
        flex-direction: column;
    }

    .sources_table{
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
        text-align: right;
    }

    .source_headline{
        text-align: left;
    }

    .article_headline{
        text-align: center;
    }

    .table_title{
        font-weight: bold;
        color: black;
        text-align: left;
        font-size: large;
        padding-top: 10px;
    }

    td{
        border-top: 1px solid gainsboro;
        padding-top: 10px;
        padding-bottom: 10px;
        text-align: right;
    }

    .sources{
        text-align:left;
    }

    .articles{
        text-align: center;
    }

    img{
        max-height:20px;
        width:auto;
    }
</style>

<main>
    <div class="stock_info_div">
        <table class="sources_table">
            <thead>
                <tr>
                    <th class = "table_title">Sentiment Sources</th>
                </tr>
                <tr>
                    <th class = "source_headline">Source</th>
                    <th class = "article_headline">Articles</th>
                    <th>Sentiment</th>
                </tr>
            </thead>
            <tbody>
                {#each stocks as stock, i}
                    <tr style = {stock.visible ? 'color: black' : 'color: lightgrey'}>
                        <td class = "sources">{stock.name}</td>
                        <td class = "articles">{stock.articles}</td>
                        <td>{stock.sentiment}</td>
                        <td>
                            <button class="eye_button" on:click={() => toggleVisibility(i)}>
                                <img src = {stock.visible ? show : hide} alt = "visibility eye button"/>
                            </button>
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
</main>