document.addEventListener("DOMContentLoaded", function() {
    const titleElement = document.getElementById("title");
    titleElement.innerHTML = titleElement.innerHTML.replace("-", "<span class='lightning'></span>");
});

// script.js
window.onload = function() {
    // Tilføj JavaScript-funktionalitet efter behov
    console.log('Dokumentet er indlæst.');
};

function gemTidspræferencerOgSkiftSide() {
    const input = document.getElementById('preferences').value;
    tidspræferencer = input.split(',').map(pref => parseInt(pref.trim(), 10));

    // Omdiriger til næste side
    window.location.href = 'elpriser9.html';
}


// Lyt efter klik på knapper
document.getElementById('skiftSideBtn').addEventListener('click', skiftSide);
document.getElementById('gaTilbageBtn').addEventListener('click', gaTilbage);

// Dynamisk ændring af iframe-kilde
var iframeElement = document.querySelector('iframe');
var dynamicURL = "https://www.elprisenligenu.dk/i/kobenhavn?mode={mode}&layout={layout}&hide-examples={hide_examples}&zoom={zoom}&background={background}";

// Opdater iframe-kilden
iframeElement.src = dynamicURL;


