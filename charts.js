async function renderChart(id, sensorType, color) {
    const res = await fetch('/api/chart/' + sensorType);
    const data = await res.json();
    const ctx = document.getElementById(id).getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: sensorType,
                data: data.values,
                borderColor: color,
                backgroundColor: color.replace('1)', '0.2)'),
                fill: true,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: { display: true },
                y: { display: true }
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    if(document.getElementById('chart-sicaklik')) renderChart('chart-sicaklik','sicaklik','rgba(255,99,132,1)');
    if(document.getElementById('chart-voltaj')) renderChart('chart-voltaj','voltaj','rgba(54,162,235,1)');
});
