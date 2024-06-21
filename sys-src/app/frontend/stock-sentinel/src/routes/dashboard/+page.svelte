<script>
    import Price from "../../components/Price.svelte";
    import Sentiment from "../../components/Sentiment.svelte";
    import Sources from "../../components/Sources.svelte";
    import Graph from "../../components/Graph.svelte";
    import GraphTest from "../../components/GraphTest.svelte";

    $: stock = "Placeholder Stock Name";
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
        <h2>{stock}</h2>
        <div class = "info">
            <div class = "price"><Price></Price></div>
            <div class = "sentiment"><Sentiment></Sentiment></div>
        </div>
        <GraphTest></GraphTest>
        <Graph></Graph>
        <Sources></Sources>
    </div>
</main>

