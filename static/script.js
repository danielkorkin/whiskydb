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
                const gameDiv = document.createElement('div');
                gameDiv.classList.add('game-result');
                gameDiv.textContent = game.name;
                gameDiv.addEventListener('click', () => {
                    window.location.href = `/game_details/${game.appid}`;
                });
                resultsDiv.appendChild(gameDiv);
            });
        });
    });
});
