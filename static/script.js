document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('searchForm').addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent the default form submission
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
            location.reload();
            // Optionally refresh the game details to reflect the new rating
        }
    })
    .catch(error => {
        console.error('Error submitting rating:', error);
        alert("There was an error submitting your rating. Please try again.");
    });
}

fetch('/rating_distribution')
    .then(response => response.json())
    .then(distribution => {
        const ctx = document.getElementById('ratingDistributionChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: Object.keys(distribution),
                datasets: [{
                    label: 'Game Compatibility Distribution',
                    data: Object.values(distribution),
                    backgroundColor: [
                        '#cd7f32', // Bronze
                        '#ffd700', // Gold
                        '#e5e4e2', // Platinum
                        '#c0c0c0', // Silver
                        '#808080' // Gray for Unsupported   
                    ],
                    hoverOffset: 4
                }]
            },
            options: {
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed !== null) {
                                    label += `${context.parsed} games (${context.formattedValue}%)`;
                                }
                                return label;
                            }
                        }
                    }
                }
            }
        });
    });
