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
        CategoryScale
    } from 'chart.js';

    ChartJS.register(
        Title,
        Tooltip,
        Legend,
        LineElement,
        LinearScale,
        PointElement,
        CategoryScale
    );

    $: data = {
        labels: ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-01-06", "2024-01-07", "2024-01-08", "2024-01-09", "2024-01-10", "2024-01-11", "2024-01-12", "2024-01-13", "2024-01-14", "2024-01-15", "2024-01-16", "2024-01-17", "2024-01-18", "2024-01-19", "2024-01-20"],
        datasets: [
            {
                label: 'Sentiment',
                data: [0.45, -0.23, 0.76, -0.34, 0.50, 0.12, -0.78, 0.36, -0.45, 0.67, -0.19, 0.85, -0.55, 0.27, -0.10, 0.53, -0.37, 0.60, -0.25, 0.80],
                borderColor: 'green',
                backgroundColor: 'green',
                borderWidth: 2,
                yAxisID: 'y',
                tension: 0.3,
                fill: true
            },
            {
                label: 'Price',
                data: [150, 145, 155, 142, 148, 151, 140, 147, 144, 153, 149, 157, 141, 150, 148, 152, 143, 154, 146, 158],
                borderColor: 'blue',
                borderWidth: 2,
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
</style>

<main>
    <Line {data} height = {700} options={{responsive: true, maintainAspectRatio: false}} />
</main>