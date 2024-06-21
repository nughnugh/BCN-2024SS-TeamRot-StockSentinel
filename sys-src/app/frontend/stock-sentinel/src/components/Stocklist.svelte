<script lang="ts">
    import thumbsUp from '$lib/assets/thumbsUp.png';
    import thumbsDown from '$lib/assets/thumbsDown.png';
    import thumbNeutral from '$lib/assets/thumbNeutral.png';
    import {
        TableBody,
        TableBodyCell,
        TableBodyRow,
        TableHead,
        TableHeadCell,
        TableSearch
    } from 'flowbite-svelte';

    let searchTerm = '';

    let stocks = [
        {name: 'Apple', ticker: 'AAPL', sentiment: 1},
        {name: 'Amazon', ticker: 'AMZN', sentiment: 1},
        {name: 'Tesla', ticker: 'TSL', sentiment: 0},
        {name: 'Random Stock', ticker: 'RST',sentiment: -1},
        {name: 'Microsoft', ticker: 'MIC',sentiment: 1},
        {name: 'Samsung', ticker: 'SMSG',sentiment: 0},
        {name: 'Another Stock', ticker: 'AST',sentiment: -1},
        {name: 'Last Stock', ticker: 'LAST',sentiment: 0}
    ]

    $: filteredStocks = stocks.filter((stock) => stock.name.toLowerCase().indexOf(searchTerm.toLowerCase()) !== -1);

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
    h2{
        padding-top: 20px;
        padding-bottom: 20px;
        font-weight: bold;
        font-size: x-large;
        color: black;
    }

    .stock_table{
        border: 1px solid gainsboro;
        border-radius: 8px;
        box-shadow: gainsboro 0 0 10px;
    }

    .table_title{
        background-color: white;
        font-size: larger;
    }

    .column_titles{
        color: grey;
        border-bottom: 1px solid gainsboro;
    }

    a:hover{
        text-decoration: underline;
    }

    img {
        max-height: 20px;
        width: auto;
        padding-left: 10px;
    }
</style>

<main>
    <h2>Stock Overview</h2>
    <div class = "stock_table">
        <TableSearch placeholder="Search stocks by name" hoverable={true} bind:inputValue={searchTerm}>
            <TableHead defaultRow={false} theadClass="text-lg">
                <tr class = "table_title">
                    <TableHeadCell colspan="3"><h3>Available Stocks</h3></TableHeadCell>
                </tr>
                <tr class="column_titles">
                    <TableHeadCell>Stock Name</TableHeadCell>
                    <TableHeadCell>Ticker</TableHeadCell>
                    <TableHeadCell  style="display: flex; align-items: center; justify-content: flex-end; padding-right: 20px;">Sentiment</TableHeadCell>
                </tr>
            </TableHead>
            <TableBody>
                {#each filteredStocks as stock}
                    <TableBodyRow>
                        <TableBodyCell tdClass="px-6 py-4 whitespace-nowrap text-base"><a href = "/dashboard">{stock.name}</a></TableBodyCell>
                        <TableBodyCell tdClass="px-6 py-4 whitespace-nowrap text-base"><a href = "/dashboard">{stock.ticker}</a></TableBodyCell>
                        <TableBodyCell style="display: flex; align-items: center; justify-content: flex-end; padding-right: 20px;">
                            {stock.sentiment}
                            <img src={chooseThumb(stock.sentiment)} alt="thumb based on sentiment"/>
                        </TableBodyCell>
                    </TableBodyRow>
                {/each}
            </TableBody>
        </TableSearch>
    </div>
</main>
