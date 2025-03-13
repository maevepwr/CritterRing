// Declare variables in the global scope
var sites, ringName, ringID, useIndex, indexPage, useRandom;

// Fetch the JSON configuration and assign values to global variables
fetch('http://127.0.0.1:1000/critterring.json')
    .then(response => response.json())
    .then(data => {
        // Assign values from the JSON response to global variables
        sites = data.RING_SITES;
        ringName = data.RING_NAME;
        ringID = data.RING_ID;
        useIndex = false; // You can set this based on additional logic
        indexPage = data.RING_INDEX;
        useRandom = true;  // You can set this based on additional logic

        // Now that variables are set, trigger the widget to load
        window.widgetDataLoaded = true; // Flag to indicate data is loaded
    })
    .catch(error => console.log('Error fetching the JSON:'));


    