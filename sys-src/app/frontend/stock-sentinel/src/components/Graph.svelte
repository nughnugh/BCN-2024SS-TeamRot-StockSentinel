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
        const response_sentiment = await fetch("http://localhost:3000/api/SentimentDataFor/" + title);
        const data_sentiment = await response_sentiment.json();
        console.log(params_price);
        console.log(data_sentiment);
        prices = params_price;
        sentiments = data_sentiment;
        for(let i = 0; i < prices.length; i++) {
            labels_graph.push(prices[i].stock_price_time);
            prices_graph.push(Number(prices[i].stock_price_val));
        }
        for(let i = 0; i < sentiments.length; i++){
            sentiments_graph.push(Math.round(Number(sentiments[i].avg_sentiment)*100)/ 100);
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
    }


    $: data = {
        labels: labels_graph,
        datasets: [
            {
                label: 'Sentiment',
                data: sentiments_graph,
                //data: [0.45, -0.23, 0.76, -0.34, 0.50, 0.12, -0.78, 0.36, -0.45, 0.67, -0.19, 0.85, -0.55, 0.27, -0.10, 0.53, -0.37, 0.60, -0.25, 0.80],
                yAxisID: 'y',
                tension: 0.3,
                borderWidth: 0,
                fill: {
                    target: 'origin',
                    above: 'rgba(0, 150, 100, 0.8)',
                    below: 'rgba(255, 0, 0, 0.8)'
                },
                pointRadius: 1
            },
            {
                label: 'Price',
                //data: [150, 145, 155, 142, 148, 151, 140, 147, 144, 153, 149, 157, 141, 150, 148, 152, 143, 154, 146, 158],
                data: prices_graph,
                borderColor: 'black',
                borderWidth: 1,
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
              options={{responsive: true, maintainAspectRatio: false}}
        />
    </div>
</main>