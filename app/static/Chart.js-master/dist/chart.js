const priceCanvas = document.getElementById('priceChart').getContext('2d');

const fetchDataAndUpdateChart = async () => {
    try {
        const response = await fetch('/real-time-chart'); // Ændre URL'en til at matche din Flask-rute
        const data = await response.json();

        // Extrahér tidspunkter og priser fra dataobjektet
        const labels = data.map(entry => entry.time_start.split('T')[1].substring(0, 5));
        const prices = data.map(entry => entry.DKK_per_kWh.toFixed(5));

        // Opret et objekt med de nye data
        const newData = {
            labels: labels,
            prices: prices
        };

        // Opdatér grafen med de nye data
        updateChartWithNewData(newData);
    } catch (error) {
        console.error('Error fetching or updating data:', error);
    }
};

// Kør fetchDataAndUpdateChart funktionen ved start for at initialisere grafen
fetchDataAndUpdateChart();

const updateChartWithNewData = (newData) => {
    const priceChart = new Chart(priceCanvas, {
        type: 'line', // Du kan ændre dette til et andet type diagram, hvis ønsket
        data: {
            labels: newData.labels,
            datasets: [{
                label: 'kr/kWh',
                stepped: true,
                borderColor: 'rgba(0,0,0,0.15)',
                pointBorderColor: 'rgba(0, 0, 0, 0)',
                pointBackgroundColor: function(ctx) {
                    let index = ctx.dataIndex;
                    let value = ctx.dataset.data[index];
                    return (value > 0.2822) ? '#c20606' : 'rgba(17, 101, 48, 1)';
                },
                data: newData.prices,
            }],
        },
        options: {
            // Tilføj eventuelle yderligere indstillinger her
        }
    });
};
