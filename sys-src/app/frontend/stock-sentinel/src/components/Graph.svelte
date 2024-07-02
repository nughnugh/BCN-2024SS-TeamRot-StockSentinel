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
    let labels_graph: string[] = [];
    let prices_graph: number[] = [];
    let sentiments_graph: number[] = [];

    onMount(async function () {
        const response_data = await fetch(__API_ADDRESS__ + "/api/historicalData/" + title);
        const historical_data = await response_data.json();
        for(let record of historical_data) {
            labels_graph.push(record.day.slice(0, 10));
            sentiments_graph.push(record.sentiment);
            prices_graph.push(record.price);
            console.log(record)
        }
        sentiments_graph = sentiments_graph
        prices_graph = prices_graph
    });

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
              options={
                  {
                      spanGaps: true,
                      responsive: true,
                      maintainAspectRatio: false,
                      scales: {
                          xAxis: {
                              display: true
                          },
                          y: {
                              min: -1,
                              max: 1
                          },
                          x: {
                              display: false,
                              ticks: {
                                  display: false
                              }
                          }
                      }
                  }
              }
        />
    </div>
</main>