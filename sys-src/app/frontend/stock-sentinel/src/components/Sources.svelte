<script lang="ts">
    import show from '$lib/assets/show.png';
    import hide from '$lib/assets/hide.png';
    import {chooseThumb} from './helper';
    import {
        Table,
        TableBody,
        TableBodyCell,
        TableBodyRow,
        TableHead,
        TableHeadCell,
    } from 'flowbite-svelte';


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
                    <TableBodyRow style = {stock.visible ? 'color: black' : 'color: lightgrey'}>
                        <TableBodyCell tdClass="px-6 py-4 whitespace-nowrap text-base">{stock.name}</TableBodyCell>
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