from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import json

app = Flask(__name__)

# Load or initialize the ratings and notes data
try:
    with open('ratings.json') as f:
        ratings = json.load(f)
except FileNotFoundError:
    ratings = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.json['query'].lower().replace('™', '').replace('©', '')
    with open('games.json', 'r') as f:
        games = json.load(f)['applist']['apps']
    filtered_games = sorted([game for game in games if query in game['name'].lower().replace('™', '').replace('©', '')],
                            key=lambda x: x['name'].lower() == query, reverse=True)[:15]
    return jsonify(filtered_games)

@app.route('/game_details/<int:appid>')
def game_details(appid):
    steam_response = requests.get(f"https://store.steampowered.com/api/appdetails?appids={appid}")
    game_details = steam_response.json().get(str(appid), {}).get('data', {})
    if not game_details:
        return "Game details not found.", 404
    game_notes = next((item for item in ratings if item['appid'] == appid), {}).get('notes', [])
    if not game_notes:
        game_notes = ["No notes available for this game."]

    game_rating_info = next((item for item in ratings if item['appid'] == appid), None)
    if game_rating_info and game_rating_info['ratings']:
        average_rating = sum(game_rating_info['ratings']) / len(game_rating_info['ratings'])
        if average_rating < 1:
            rating_category = "Unsupported"
        elif average_rating < 2:
            rating_category = "Bronze"
        elif average_rating < 3:
            rating_category = "Silver"
        elif average_rating < 4:
            rating_category = "Gold"
        else:
            rating_category = "Platinum"
    else:
        average_rating = 0
        rating_category = "Unsupported"
    
    return render_template('game_details.html', game=game_details, notes=game_notes, average_rating=average_rating, rating_category=rating_category)


@app.route('/rate_game', methods=['POST'])
def rate_game():
    content = request.json
    appid = content['appid']
    rating = content['rating']
    notes = content.get('notes', '')
    found = False
    appid = int(appid)
    rating = int(rating)
    
    for game_rating in ratings:
        if game_rating['appid'] == appid:
            game_rating['ratings'].append(rating)
            if notes:
                game_rating['notes'] = notes
            found = True
            break
    
    if not found:
        ratings.append({"appid": appid, "ratings": [rating], "notes": notes})
    
    with open('ratings.json', 'w') as f:
        json.dump(ratings, f, indent=4)
    
    return jsonify({"success": True})

@app.route('/add_note/<int:appid>', methods=['POST'])
def add_note(appid):
    new_note = request.form['note']
    if new_note:
        for game in ratings:
            if game['appid'] == appid:
                if 'notes' not in game or not isinstance(game['notes'], list):
                    game['notes'] = []
                game['notes'].append(new_note)
                break
        else:
            # If the game is not found in ratings, add a new entry
            ratings.append({"appid": appid, "ratings": [], "notes": [new_note]})
    
        with open('ratings.json', 'w') as f:
            json.dump(ratings, f, indent=4)

    return redirect(url_for('game_details', appid=appid))

@app.route('/rating_distribution')
def rating_distribution():
    distribution = {'Unsupported': 0, 'Bronze': 0, 'Silver': 0, 'Gold': 0, 'Platinum': 0}
    for game in ratings:
        average_rating = sum(game['ratings']) / len(game['ratings']) if game['ratings'] else 0
        if average_rating < 1:
            distribution['Unsupported'] += 1
        elif average_rating < 2:
            distribution['Bronze'] += 1
        elif average_rating < 3:
            distribution['Silver'] += 1
        elif average_rating < 4:
            distribution['Gold'] += 1
        else:
            distribution['Platinum'] += 1
    return jsonify(distribution)

if __name__ == '__main__':
    app.run(debug=True)
