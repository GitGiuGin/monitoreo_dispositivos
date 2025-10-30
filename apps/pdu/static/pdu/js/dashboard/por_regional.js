import { colores } from './colores_grafica.js';

new Chart(document.getElementById('chartRegional'), {
    type: 'bar',
    data: {
        labels: labelsRegional,
        datasets: datasetsRegional.map((dataset, i) => ({
            label: dataset.label,
            data: dataset.data,
            backgroundColor: colores[i % colores.length],
            borderColor: colores[i % colores.length],
            borderWidth: 1
        }))
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'right',
                labels: {
                    usePointStyle: true,
                    pointStyle: 'circle',
                    boxWidth: 12,
                }
            },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        return `${context.dataset.label}: ${context.formattedValue}`;
                    }
                }
            }
        },
        scales: {
            x: {
                stacked: true,
                grid: { display: false }
            },
            y: {
                stacked: true,
                beginAtZero: true
            }
        }
    }
});