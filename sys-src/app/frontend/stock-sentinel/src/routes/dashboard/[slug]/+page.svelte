<script lang="ts">
    import Price from "../../../components/Price.svelte";
    import Sentiment from "../../../components/Sentiment.svelte";
    import Sources from "../../../components/Sources.svelte";
    import Graph from "../../../components/Graph.svelte";

    export let data;
    let title:string = data.title;

</script>

<style>
    .dashboard{
        display: flex;
        flex-direction: column;
        font-family: "Montserrat", sans-serif;
        padding-left: 50px;
        padding-right: 50px;
    }

    h2{
        font-size: x-large;
        font-weight: bold;
        padding-top: 20px;
        padding-bottom: 20px;
    }

    .info{
        display: flex;
        margin-bottom: 25px;
    }

    .price{
        flex: 1;
        margin-right: 25px;
    }

    .sentiment{
        flex:1;
        margin-left: 25px;
    }
</style>


<main>
    <div class = "dashboard">
        <h2>{data.title}</h2>
        <div class = "info">
            <div class = "price"><Price bind:title></Price></div>
            <div class = "sentiment"><Sentiment bind:title></Sentiment></div>
        </div>
        <Graph bind:title></Graph>
        <Sources bind:title></Sources>
    </div>
</main>

