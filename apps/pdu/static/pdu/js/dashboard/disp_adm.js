    new Chart(document.getElementById('chartAdm'), {
        type: 'doughnut',
        data: {
            labels: admLabels,
            datasets: [{
                label: 'Cantidad de dispositivos',
                data: admTotals,
                backgroundColor: ['#f44336', '#4caf50'],
                borderColor: ['#c62828', '#388e3c'],
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
                },
            },
        }
    });