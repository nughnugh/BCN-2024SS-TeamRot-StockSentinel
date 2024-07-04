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
    import dateFormat from 'dateformat';

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
    let grouping_value: number = 1;

    async function loadGraph() {
        const response_data = await fetch(`${__API_ADDRESS__}/api/historicalDataInRange?stockName=${encodeURIComponent(title)}&groupingTime=${grouping_value}`);
        const historical_data = await response_data.json();
        sentiments_graph = [];
        labels_graph = [];
        prices_graph = [];
        for(let record of historical_data) {
            labels_graph.push(dateFormat(new Date(record.day), 'yyyy-mm-dd'));
            sentiments_graph.push(record.sentiment);
            prices_graph.push(record.price);
        }
        sentiments_graph = sentiments_graph
        prices_graph = prices_graph
    }

    onMount(() => loadGraph());

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
        box-shadow: gainsboro 0 0 10px;
    }

    h2{
        font-weight: bold;
        font-size: larger;
    }

    input {
        border: 1px solid gainsboro;
        border-radius: 8px;
        margin-top: 0.5rem;
    }
</style>

<main>
    <h2>Historical Sentiment and Price</h2>
    <label for="groupingInput">Sentiment Grouping:</label>
    <input
            type="number"
            inputmode="numeric"
            min="1"
            max="30"
            name="groupingInput"
            bind:value={grouping_value}
            on:input|preventDefault={loadGraph}
    />

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
                      },
                      transitions: {
                          hide: {
                              animation: {
                                  duration: 0,
                              }
                          },
                          show: {
                              animation: {
                                  duration: 0
                              }
                          }
                      }
                  }
              }
        />
    </div>
</main>