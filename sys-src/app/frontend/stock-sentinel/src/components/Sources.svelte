<script lang="ts">
    import show from '$lib/assets/show.png';
    import hide from '$lib/assets/hide.png';
    import {chooseThumb} from './helper';

    let stocks = [
        {name: 'source1', articles: 1, sentiment: 1, visible: true},
        {name: 'source2', articles: 2, sentiment: 1, visible: true},
        {name: 'source3', articles: 3, sentiment: 0, visible: true},
        {name: 'source4', articles: 4, sentiment: -1, visible: true},
        {name: 'source5', articles: 5, sentiment: 1, visible: true},
        {name: 'source6', articles: 6, sentiment: 0, visible: true},
        {name: 'source7', articles: 7, sentiment: -1, visible: true},
        {name: 'source8', articles: 8, sentiment: 1, visible: true},
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
        border-radius: 8px;
        border-collapse: collapse;
        box-shadow: grey 0 0 10px;
    }

    th{
        padding-left: 20px;
        padding-right: 20px;
        font-weight: bold;
        color: darkgrey;
        padding-bottom: 10px;
        text-align: right;
    }

    .table_title{
        font-weight: bold;
        color: black;
        text-align: left;
        font-size: large;
        padding-top: 15px;
    }

    td{
        border-top: 1px solid gainsboro;
        padding: 10px 20px;
        text-align: right;
    }

    .sources{
        text-align:left;
        width: fit-content;
    }

    .articles{
        text-align: center;
        width: auto;
    }

    .sentiment{
        width: 10%;
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
                    <th class = "sources">Source</th>
                    <th class = "articles">Articles</th>
                    <th class = "sentiment">Sentiment</th>
                </tr>
            </thead>
            <tbody>
                {#each stocks as stock, i}
                    <tr style = {stock.visible ? 'color: black' : 'color: lightgrey'}>
                        <td class = "sources">{stock.name}</td>
                        <td class = "articles">{stock.articles}</td>
                        <td class = "sentiment"><img src={chooseThumb(stock.sentiment)} alt = "thumb based on sentiment"/></td>
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