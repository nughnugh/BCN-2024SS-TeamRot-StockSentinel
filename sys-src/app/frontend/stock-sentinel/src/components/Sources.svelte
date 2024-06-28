<script lang="ts">
    import {chooseThumb} from './helper';
    import {
        Table,
        TableBody,
        TableBodyCell,
        TableBodyRow,
        TableHead,
        TableHeadCell,
    } from 'flowbite-svelte';

    import {onMount} from "svelte";

    let sentiment:number;

    export let title:string;

    let stocks: Stock[] = [];

    onMount(async function () {
        const response = await fetch(__API_ADDRESS__ + "/api/ArticlesBySourceFor/" + title);
        const data = await response.json();
        console.log(data);
        stocks = data;
    });
    interface Stock{
        ticker_symbol: string;
        source_url: string;
        articles: string;
        sentiment: string;
    }

</script>

<style>
    h2{
        padding: 20px;
        font-weight: bold;
        color: black;
    }

    .sources_table{
        border: 1px solid gainsboro;
        border-radius: 8px;
        box-shadow: gainsboro 0 0 10px;
        margin-bottom: 50px;
    }

    .column_titles{
        color: grey;
        border-bottom: 1px solid gainsboro;
    }

    img {
        max-height: 20px;
        width: auto;
        padding-left: 10px;
    }

    a:hover{
        text-decoration: underline;
    }
</style>

<main>
    <div class="sources_table">
        <h2>Sources Used</h2>
        <Table>
            <TableHead defaultRow={false} theadClass="text-base">
                <tr class="column_titles">
                    <TableHeadCell>Source</TableHeadCell>
                    <TableHeadCell style = "text-align: center;">Articles</TableHeadCell>
                    <TableHeadCell style="display: flex; align-items: center; justify-content: flex-end; padding-right: 20px;">Sentiment</TableHeadCell>
                </tr>
            </TableHead>
            <TableBody>
                {#each stocks as stock, i}
                    <TableBodyRow>
                        <TableBodyCell tdClass="px-6 py-4 whitespace-nowrap text-base"><a href = "https://{stock.source_url}">{stock.source_url}</a></TableBodyCell>
                        <TableBodyCell tdClass="px-6 py-4 whitespace-nowrap text-base" style = "text-align: center;">{stock.articles}</TableBodyCell>
                        <TableBodyCell style="display: flex; align-items: center; justify-content: flex-end; padding-right: 20px;">
                            <img src={chooseThumb(stock.sentiment)} alt = "thumb based on sentiment"/>
                        </TableBodyCell>
                    </TableBodyRow>
                {/each}
            </TableBody>
        </Table>
    </div>
</main>