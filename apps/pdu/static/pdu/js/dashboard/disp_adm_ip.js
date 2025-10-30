new Chart(document.getElementById('chartAdmIP'), {
    type: 'doughnut',
    data: {
        labels: admIPData.labels,
        datasets: [{
            label: 'Cantidad de dispositivos',
            data: admIPData.totals,
            backgroundColor: ['#4caf50', '#f44336'],
            borderColor: ['#388e3c', '#c62828'],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { 
                position: 'right',
                
            },
        }
    }
});