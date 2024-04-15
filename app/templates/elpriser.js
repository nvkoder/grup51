// Funksjon for å oppdatere søylediagrammet med nye elpriser
function oppdaterDiagram() {
    // Kall til backend for å hente elpriser
    fetch('/elpriser')
        .then(response => response.json())
        .then(data => {
            // Eksempeldata for elpriser (kan erstattes med data fra backend)
            var elpriser = data.map(entry => entry.DKK_per_kWh); // Henter ut DKK_per_kWh fra data

            // Opretter dataobjekt for søylediagrammet
            var data = [{
                x: data.map((_, i) => i + 1), // Timeintervaller
                y: elpriser,
                type: 'bar'
            }];

            // Opretter layoutobjekt for søylediagrammet
            var layout = {
                title: 'Elpriser',
                xaxis: { title: 'Time' },
                yaxis: { title: 'Pris (DKK/kWh)' }
            };

            // Oppdaterer søylediagrammet med ny data og layout
            Plotly.newPlot('søylediagram', data, layout); // Riktig staving av søylediagram
        })
        .catch(error => console.error('Feil ved henting av elpriser:', error)); // Håndtering av feil
}

// Oppdater søylediagrammet i sanntid (hvert 5. sekund)
setInterval(oppdaterDiagram, 5000);

// Kall funksjonen for å oppdatere diagrammet ved siden av den initielle visningen
oppdaterDiagram();
