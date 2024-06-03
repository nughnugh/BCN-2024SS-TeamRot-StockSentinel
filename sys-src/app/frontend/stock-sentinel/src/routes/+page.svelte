<script>
    let price = "$Placeholder"
</script>

<style>
    .grid-container {
        display: grid;
    }
    .header{
        display: grid;
        grid-column: 1;
        grid-row: 1;
        text-align: left;
        border-style: solid;
        align-items: baseline;
    }
    .title{
        grid-column: 1;
        text-align: left;
    }
    .pages{
        grid-align: center;
        grid-column: 2;
    }
    .stock_name{
        grid-column: 1;
        grid-row: 2;
    }
    .stock_info{
        grid-column: 1;
        grid-row: 3;
        border-style: solid;
    }
    .side_blocker{
        grid-column-start: 1;
        grid-column-end: 3;
        grid-row: 2;
    }

</style>

<div class="grid-container">

    <div class="header">
        <div class="title"> <h1>Stock Sentinel </h1></div>  <div class="pages"> Overview</div>
    </div>
    <div class = "stock_name">
        <h2>Stock Name</h2>
    </div>
    <div class = "stock_info">
        <div> <h3> Current Price</h3> </div>
        <div> <h2>{price}</h2></div>
        <div> <p>Price at Market Close</p></div>
    </div>

    <div class = "side_blocker"></div>

</div>