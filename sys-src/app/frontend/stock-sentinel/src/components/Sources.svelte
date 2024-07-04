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
    import hide from "$lib/assets/hide.png";
    import show from "$lib/assets/show.png";

    let sentiment:number;

    export let title:string;

    let sources: Source[] = [];

    onMount(async function () {
        const response = await fetch(__API_ADDRESS__ + "/api/ArticlesBySourceFor/" + title);
        const data = await response.json();
        console.log(data);
        sources = data;
    });

    interface Source {
        source_url: string;
        visible: boolean;
        articles: string;
        sentiment: string;
    }

    function toggleVisibility(index: number){
        sources[index].visible = !sources[index].visible;
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
                    <TableHeadCell style = "text-align: center;">Sentiment</TableHeadCell>
                    <TableHeadCell style = "display: flex; align-items: center; justify-content: flex-end; padding-right: 20px;">Visibility</TableHeadCell>
                </tr>
            </TableHead>
            <TableBody>
                {#each sources as stock, i}
                    <TableBodyRow>
                        <!-- <TableBodyCell tdClass="px-6 py-4 whitespace-nowrap text-base"><a href = "/dashboard/{title}/{stock.source_url}">{stock.source_url}</a></TableBodyCell> -->
                        <TableBodyCell tdClass="px-6 py-4 whitespace-nowrap text-base"><a href = "https://{stock.source_url}">{stock.source_url}</a></TableBodyCell>
                        <TableBodyCell tdClass="px-6 py-4 whitespace-nowrap text-base" style = "text-align: center;">{stock.articles}</TableBodyCell>
                        <TableBodyCell tdClass="px-6 py-4 whitespace-nowrap text-base">
                            <div style = "display: flex; justify-content: center;">
                            <img src={chooseThumb(stock.sentiment)} alt = "thumb based on sentiment"/>
                            </div>
                        </TableBodyCell>
                        <TableBodyCell>
                            <div  style="display: flex; justify-content: flex-end;">
                            <button class="eye_button" on:click={() => toggleVisibility(i)}>
                                <img src = {stock.visible ? show : hide} alt = "visibility eye button"/>
                            </button>
                            </div>
                        </TableBodyCell>
                    </TableBodyRow>
                {/each}
            </TableBody>
        </Table>
    </div>
</main>