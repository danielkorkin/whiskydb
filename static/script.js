document.getElementById('searchForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const query = document.getElementById('searchQuery').value;
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({query: query})
    }).then(response => response.json())
    .then(data => {
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = ''; // Clear previous results
        data.forEach(game => {
            const div = document.createElement('div');
            div.textContent = game.name; // Display game name
            // Add more game details here
            resultsDiv.appendChild(div);
        });
    });
});
