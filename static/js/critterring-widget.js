// Declare variables in the global scope
var sites, ringName, ringID, useIndex, indexPage, useRandom, dataRaw;

// Main function that contains the widget logic
function main() {
    var tag = document.getElementById(ringID); // Find the widget on the page
    thisSite = window.location.href; // Get the URL of the site we're currently on
    thisIndex = null;

    // Go through the site list to see if this site is on it and find its position
    for (i = 0; i < sites.length; i++) {
        if (thisSite.startsWith(sites[i])) { // We use startsWith so this will match any subdirectory
            thisIndex = i;
            break; // When we've found the site, we don't need to search anymore
        }
    }

    function randomSite() {
        otherSites = sites.slice(); // Create a copy of the sites list
        otherSites.splice(thisIndex, 1); // Remove the current site so we don't just land on it again
        randomIndex = Math.floor(Math.random() * otherSites.length);
        location.href = otherSites[randomIndex];
    }

    // If we didn't find the site in the list, display a warning
    if (thisIndex == null) {
        tag.insertAdjacentHTML('afterbegin', `
            This site is not in the webring
        `);
    } else {
        // Find the 'next' and 'previous' sites in the ring
        previousIndex = (thisIndex - 1 < 0) ? sites.length - 1 : thisIndex - 1;
        nextIndex = (thisIndex + 1 >= sites.length) ? 0 : thisIndex + 1;

        indexText = ""
        // If you've chosen to include an index, this builds the link to that
        if (useIndex) {
            indexText = `<a href='${indexPage}'>index</a> | `;
        }

        randomText = ""
        // If you've chosen to include a random button, this builds the link that does that
        if (useRandom) {
            randomText = `<a href='javascript:void(0)' onclick='randomSite()'>random</a> | `;
        }

        // This is the code that displays the widget
        fetch('http://127.0.0.1:1000/critterring-widget.html')
            .then(response => response.text())
            .then(html => tag.insertAdjacentHTML('afterbegin', html))
            .catch(error => console.error('Error loading the widget:', error));
    }
}

// Fetch the JSON configuration and assign values to global variables
fetch('http://127.0.0.1:1000/critterring.json')
    .then(response => response.json())
    .then(data => {
        data = JSON.parse(data);
        // Assign values from the JSON response to global variables
        sites = data.RING_SITES;
        ringName = data.RING_NAME;
        ringID = data.RING_ID;
        useIndex = false; // You can set this based on additional logic
        indexPage = data.RING_INDEX;
        useRandom = true;  // You can set this based on additional logic

        // Now that variables are set, trigger the main function to load the widget
        window.widgetDataLoaded = true; // Flag to indicate data is loaded
        main()
    })
    .catch(error => console.log('Error fetching the JSON:', error));


    $(document).ready(function() {
        function updateCurrentPage() {
            $('.page').css('display', 'none');
            var selectedRadio = $('input[type="radio"][name="page"]:checked');
            var selectedId = selectedRadio.attr('id');
            if (selectedId) {
                $('#' + selectedId + 'Content').css('display', 'block');
            }
        }


        function updateAuthFormContent() {
            $('.authFormContent').css('display', 'none');
            var selectedRadio = $('input[type="radio"][name="authForms"]:checked');
            var selectedName = selectedRadio.attr('id');
            var selectedElement = $('#' + selectedName + 'Content');
            console.log(selectedElement)
            if (selectedElement) {
                selectedElement.css('display', 'flex');
            }
        }


        $(document).on('change', 'input[type="radio"][name="page"]', updateCurrentPage);
        updateCurrentPage();

        $(document).on('change', 'input[type="radio"][name="authForms"]', updateAuthFormContent);
        updateAuthFormContent()

    });
    