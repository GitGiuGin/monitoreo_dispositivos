import { colores } from './colores_grafica.js';

new Chart(document.getElementById('chartAdmRegional'), {
    type: 'bar',
    data: {
        labels: admRegionalData.labels,
        datasets: admRegionalData.datasets.map((ds, i) => ({
            ...ds,
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