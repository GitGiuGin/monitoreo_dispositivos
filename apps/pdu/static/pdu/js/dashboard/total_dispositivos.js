import { colores } from './colores_grafica.js';

const labelsTipo = porTipo.map(item => item['modelo__marca__dispositivo'] || 'Desconocido');
const valoresTipo = porTipo.map(item => item.total);

// Asignar colores, gris si es "Desconocido"
const backgroundColors = labelsTipo.map((label, i) =>
    label === 'Desconocido' ? '#B0B0B0' : colores[i % colores.length]
);
const borderColors = labelsTipo.map((label, i) =>
    label === 'Desconocido' ? '#808080' : colores[i % colores.length]
);

new Chart(document.getElementById('chartTotal'), {
    type: 'doughnut',
    data: {
        labels: labelsTipo,
        datasets: [{
            label: 'Cantidad de Dispositivos',
            data: valoresTipo,
            backgroundColor: backgroundColors,
            borderColor: borderColors,
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { 
                position: 'right',
                labels: {
                    usePointStyle: true,
                    pointStyle: 'circle',
                    boxWidth: 12,
                }
            }
        }
    }
});