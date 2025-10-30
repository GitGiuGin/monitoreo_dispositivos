import { colores } from './colores_grafica.js';

const labelsCiudad = dataCiudad.map(item => item['ubicacion__ciudad__nombre']);
const valoresCiudad = dataCiudad.map(item => item.total);

new Chart(document.getElementById('chartCiudad'), {
    type: 'bar',
    data: {
        labels: labelsCiudad,
        datasets: [{
            label: 'Cantidad de dispositivos',
            data: valoresCiudad,
            backgroundColor: labelsCiudad.map((_, i) => colores[i % colores.length]),
            borderColor: labelsCiudad.map((_, i) => colores[i % colores.length]),
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { display: false },
        },
        scales: {
            x: {
                stacked: false,
                grid: { display: false }
            },
            y: {
                beginAtZero: true
            }
        }
    }
});