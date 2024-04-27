function fetchMatches(trackName, artistName, trackElementId) {
    fetch('/get-matches', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({trackName: trackName, artistName: artistName}),
    })
    .then(response => response.json())
    .then(data => {
        const dropdown = createDropdown(data.matches, trackElementId);
        document.getElementById(trackElementId).appendChild(dropdown);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function createDropdown(matches, trackElementId) {
    const select = document.createElement('select');
    select.id = `match-select-${trackElementId}`;
    matches.forEach(match => {
        const option = document.createElement('option');
        option.value = match.id; // Assuming each match has an ID
        option.textContent = `${match.title} by ${match.artist}`;
        select.appendChild(option);
    });

    // Optional: add a default "Select a match" option
    const defaultOption = document.createElement('option');
    defaultOption.selected = true;
    defaultOption.disabled = true;
    defaultOption.textContent = "Select a match";
    select.insertBefore(defaultOption, select.firstChild);

    // Append a checkmark button for confirming the selection
    const checkButton = document.createElement('button');
    checkButton.textContent = '✔';
    checkButton.onclick = () => confirmMatch(trackElementId, select.value);

    const container = document.createElement('div');
    container.appendChild(select);
    container.appendChild(checkButton);
    return container;
}

function confirmMatch(trackElementId, matchId) {
    // Implement the logic to confirm the match
    // This might involve sending the matchId back to the server to update the database
    console.log(`Confirmed match ${matchId} for track ${trackElementId}`);
    // Example of sending the confirmed match back to the server
    fetch('/confirm-match', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({trackElementId: trackElementId, matchId: matchId}),
    })
    .then(response => response.json())
    .then(data => {
        // Handle response, e.g., update UI to show the match is confirmed
        console.log(data.message); // Assuming the server sends back a confirmation message
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}


function manualMatch(trackName, artistName, trackElementId) {
    fetch('/manual-match', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({trackName: trackName, artistName: artistName}),
    })
    .then(response => response.json())
    .then(data => {
        // Assuming `data` contains the list of possible matches
        // Update the DOM with these matches and allow the user to select one
        // This is an example and would need to be expanded based on your application's structure
        const trackElement = document.getElementById(trackElementId);
        trackElement.innerHTML += "<select onchange='submitMatch(this.value)'>" + data.matches.map(match => `<option value="${match.id}">${match.title} by ${match.artist}</option>`).join('') + "</select>";
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}