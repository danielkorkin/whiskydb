from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Load or initialize ratings data
try:
    with open('ratings.json') as f:
        ratings = json.load(f)
except FileNotFoundError:
    ratings = []

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for searching games
@app.route('/search', methods=['POST'])
def search():
    query = request.json['query'].lower().replace('™', '').replace('©', '')
    with open('games.json', 'r') as f:
        games = json.load(f)['applist']['apps']
    filtered_games = sorted([game for game in games if query in game['name'].lower().replace('™', '').replace('©', '')],
                            key=lambda x: x['name'].lower() == query, reverse=True)[:15]
    return jsonify(filtered_games)

# Route for fetching game details
@app.route('/game_details/<int:appid>')
def game_details(appid):
    steam_response = requests.get(f"https://store.steampowered.com/api/appdetails?appids={appid}")
    game_details = steam_response.json().get(str(appid), {}).get('data', {})
    if not game_details:
        return "Game details not found.", 404
    game_rating = next((item for item in ratings if item['appid'] == appid), None)
    if game_rating:
        average_rating = sum(game_rating['ratings']) / len(game_rating['ratings'])
    else:
        average_rating = "Not Rated"
    return render_template('game_details.html', game=game_details, average_rating=average_rating)

# Route for submitting ratings
@app.route('/rate_game', methods=['POST'])
def rate_game():
    appid = request.json['appid']
    rating = request.json['rating']
    game_rating = next((item for item in ratings if item['appid'] == appid), None)
    if game_rating:
        game_rating['ratings'].append(rating)
    else:
        ratings.append({"appid": appid, "ratings": [rating]})
    with open('ratings.json', 'w') as f:
        json.dump(ratings, f)
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)
