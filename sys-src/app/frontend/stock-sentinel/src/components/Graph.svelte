<script>
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

    $: data = {
        labels: ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-01-06", "2024-01-07", "2024-01-08", "2024-01-09", "2024-01-10", "2024-01-11", "2024-01-12", "2024-01-13", "2024-01-14", "2024-01-15", "2024-01-16", "2024-01-17", "2024-01-18", "2024-01-19", "2024-01-20"],
        datasets: [
            {
                label: 'Sentiment',
                data: [0.45, -0.23, 0.76, -0.34, 0.50, 0.12, -0.78, 0.36, -0.45, 0.67, -0.19, 0.85, -0.55, 0.27, -0.10, 0.53, -0.37, 0.60, -0.25, 0.80],
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
                data: [150, 145, 155, 142, 148, 151, 140, 147, 144, 153, 149, 157, 141, 150, 148, 152, 143, 154, 146, 158],
                borderColor: 'black',
                borderWidth: 1,
                pointRadius: 1,
                tension:0.2,
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
        <Line {data} height = {700} options={{responsive: true, maintainAspectRatio: false}} />
    </div>
</main>