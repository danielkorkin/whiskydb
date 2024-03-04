from flask import Flask, render_template, request, jsonify, url_for
import json
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.json['query'].lower().replace('™', '').replace('©', '')
    with open('games.json', 'r') as f:
        games = json.load(f)['applist']['apps']
    filtered_games = [game for game in games if query in game['name'].lower().replace('™', '').replace('©', '')]
    filtered_games = sorted(filtered_games, key=lambda x: x['name'].lower() == query, reverse=True)[:15]
    return jsonify(filtered_games)

@app.route('/game_details/<int:appid>')
def game_details(appid):
    response = requests.get(f"https://store.steampowered.com/api/appdetails?appids={appid}")
    data = response.json()[str(appid)]['data']
    return jsonify({"name": data['name'], "header_image": data['header_image'], "release_date": data['release_date']['date']})

@app.route('/ratings/<int:appid>', methods=['POST'])
def rate_game(appid):
    rating = request.json['rating']
    try:
        with open('ratings.json', 'r+') as f:
            ratings = json.load(f)
            game_rating = next((item for item in ratings if item['appid'] == appid), None)
            if game_rating:
                game_rating['ratings'].append(rating)
            else:
                ratings.append({"appid": appid, "ratings": [rating]})
            f.seek(0)
            json.dump(ratings, f, indent=4)
            f.truncate()
    except FileNotFoundError:
        with open('ratings.json', 'w') as f:
            json.dump([{"appid": appid, "ratings": [rating]}], f, indent=4)
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)
