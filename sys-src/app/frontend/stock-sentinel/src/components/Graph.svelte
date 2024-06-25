<script lang="ts">
    import { Line } from 'svelte-chartjs';
    import{
        Chart as ChartJS,
        Title,
        Tooltip,
        Legend,
        LineElement,
        LinearScale,
        PointElement,
        CategoryScale,
        Filler
    } from 'chart.js';

    ChartJS.register(
        Title,
        Tooltip,
        Legend,
        LineElement,
        LinearScale,
        PointElement,
        CategoryScale,
        Filler
    );

    import {onMount} from "svelte";

    export let title:string;
    let prices: Price[];
    let labels_graph: string[] = [];
    let prices_graph: number[] = [];
    let sentiments: Stock[] = [];
    let sentiments_graph: number[] = [];

    onMount(async function () {
        const response_price = await fetch("http://localhost:3000/api/StockDataFor/"+ title);
        const params_price = await response_price.json();
        const response_sentiment = await fetch("http://localhost:3000/api/historicalSentiments/" + title);
        const data_sentiment = await response_sentiment.json();
        console.log(params_price);
        console.log(data_sentiment);
        prices = params_price;
        sentiments = data_sentiment;
        for(let i = prices.length-1; i >= 0; i--) {
            prices_graph.push(Number(prices[i].stock_price_val));
        }
        for(let i = sentiments.length-1; i >= 0; i--){
            let sentiment = Math.round(Number(sentiments[i].avg_sentiment)*100)/ 100
            sentiments_graph.push(sentiment);
            labels_graph.push(sentiments[i].pub_date.slice(0, 10));
        }
    });

    interface Price{
        stock_price_val: string;
        stock_price_time: string;
    }

    interface Stock{
        name: string;
        ticker_symbol: string;
        avg_sentiment: string;
        pub_date: string;
    }


    $: data = {
        labels: labels_graph,
        datasets: [
            {
                label: 'Sentiment',
                data: sentiments_graph,
                yAxisID: 'y',
                tension: 0.3,
                borderWidth: 0,
                fill: {
                    target: 'origin',
                    above: 'rgba(0, 150, 100, 0.7)',
                    below: 'rgba(255, 0, 0, 0.7)'
                },
                pointRadius: 1
            },
            {
                label: 'Price',
                data: prices_graph,
                borderColor: 'black',
                borderWidth: 2,
                pointRadius: 1,
                tension:0.3,
                fill: false,
                yAxisID: 'y1'
            }
        ]
    };

</script>

<style>
    main{
        border: 1px solid gainsboro;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 50px;
    }

    h2{
        font-weight: bold;
        font-size: larger;
    }
</style>

<main>
    <h2>Historical Sentiment and Price</h2>
    <div class="graph">
        <Line data = {data}
              height = {700}
              options={{responsive: true, maintainAspectRatio: false, scales: {xAxes: {display: false},yAxes: {display: false}}}}
        />
    </div>
</main>