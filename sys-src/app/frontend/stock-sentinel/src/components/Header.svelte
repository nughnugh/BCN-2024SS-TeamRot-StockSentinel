<script>
    import StockSentinel from "$lib/assets/StockSentinel.png";
</script>

<style>
    header{
        position: sticky;
        top: 0;
        left: 0;
        display: flex;
        flex-direction: row;
        justify-content: left;
        align-items: center;
        width: 100%;
        border-bottom: gainsboro solid 2px;
        font-family: "Montserrat", sans-serif;
        margin-top: 0;
        padding: 20px;
        box-shadow: gainsboro 0 0 10px;
        background-color: white;
        font-size: larger;
    }

    .title{
        padding-right: 50px;
        padding-left: 50px;
        font-weight: bold;
    }

    nav a{
        text-decoration: none;
        color: grey;
        font-weight: bold;
        padding: 10px;
    }

    nav a:hover{
        background-color: darkgrey;
        color: white;
        border-radius: 5px;
        padding: 10px;
    }

    img{
        max-height: 40px;
    }
</style>

<header>
    <div class = "title">
        <img src ={StockSentinel} alt = "Stock Sentinel Logo"/>
    </div>
    <nav>
        <a href = "/">Overview</a>
    </nav>
</header>
