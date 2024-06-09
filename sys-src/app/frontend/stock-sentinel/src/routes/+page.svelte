<script>
    import Header from "../components/Header.svelte";
    import StockInfo from "../components/StockInfo.svelte";
    import Sentiment from "../components/Sentiment.svelte";
    import Sources from "../components/Sources.svelte";
</script>

<style>
    .info{
        display:grid;
        grid-template-columns: 1fr 1fr;
        grid-gap:20px;
    }
</style>


<main>
    <div class = "dashboard">
        <Header></Header>
        <div class = "info">
            <StockInfo></StockInfo>
            <Sentiment></Sentiment>
        </div>
        <Sources></Sources>
    </div>
</main>

