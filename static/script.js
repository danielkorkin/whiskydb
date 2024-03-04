document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('searchBtn').addEventListener('click', function() {
        const query = document.getElementById('searchQuery').value;
        fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({query: query})
        })
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '';
            data.forEach(game => {
                const div = document.createElement('div');
                div.textContent = game.name;
                div.classList.add('game-result');
                div.onclick = () => window.location.href = `/game_details/${game.appid}`;
                resultsDiv.appendChild(div);
            });
        });
    });
});

function submitRating(element) {
    var appid = element.dataset.appid;
    var rating = element.dataset.rating;
    fetch(`/rate_game`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({appid: appid, rating: rating})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Rating submitted successfully!");
            // Optionally refresh the game details to reflect the new rating
        }
    })
    .catch(error => {
        console.error('Error submitting rating:', error);
        alert("There was an error submitting your rating. Please try again.");
    });
}
