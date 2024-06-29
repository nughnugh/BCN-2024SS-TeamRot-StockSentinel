<script lang="ts">
    import Articles from "../../../../components/Articles.svelte";
    import Sentiment from "../../../../components/Sentiment.svelte";
    import Sources from "../../../../components/Sources.svelte";
    import Graph from "../../../../components/Graph.svelte";
    import Price from "../../../../components/Price.svelte";

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

</style>


<main>
    <div class = "dashboard">
        <h2>{data.title}</h2>
        <Articles bind:title></Articles>
    </div>
</main>