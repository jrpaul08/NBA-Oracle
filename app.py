from flask import Flask, render_template, jsonify, send_from_directory
import requests
from datetime import datetime, timedelta
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model
try:
    model = joblib.load('bball_game_winner_predictor_compatible.pkl')
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

# ESPN API headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def get_upcoming_games(max_games=4):
    """Get upcoming NBA games from ESPN API"""
    try:
        url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            games = []
            
            for event in data.get('events', [])[:max_games]:
                competition = event.get('competitions', [{}])[0]
                competitors = competition.get('competitors', [])
                
                if len(competitors) >= 2:
                    home_team = next((c.get('team', {}) for c in competitors if c.get('homeAway') == 'home'), {})
                    away_team = next((c.get('team', {}) for c in competitors if c.get('homeAway') == 'away'), {})
                    
                    if home_team and away_team:
                        games.append({
                            'game_id': str(event.get('id', '')),
                            'date': event.get('date', '')[:10],
                            'time': event.get('status', {}).get('type', {}).get('shortDetail', 'TBD'),
                            'home_team': home_team.get('displayName', ''),
                            'away_team': away_team.get('displayName', ''),
                            'home_team_abbr': home_team.get('abbreviation', ''),
                            'away_team_abbr': away_team.get('abbreviation', '')
                        })
            
            if games:
                return games
    except Exception as e:
        print(f"Error fetching games: {e}")
    
    # Fallback sample data
    today = datetime.now()
    return [
        {
            'game_id': 'sample1',
            'date': today.strftime('%Y-%m-%d'),
            'time': '8:00 PM ET',
            'home_team': 'Los Angeles Lakers',
            'away_team': 'Golden State Warriors',
            'home_team_abbr': 'LAL',
            'away_team_abbr': 'GSW'
        },
        {
            'game_id': 'sample2',
            'date': (today + timedelta(days=1)).strftime('%Y-%m-%d'),
            'time': '7:30 PM ET',
            'home_team': 'Boston Celtics',
            'away_team': 'Miami Heat',
            'home_team_abbr': 'BOS',
            'away_team_abbr': 'MIA'
        }
    ]

def predict_game_winner(home_team, away_team):
    """Predict the winner using the trained model"""
    try:
        if model is None:
            return {"error": "Model Prediction Failure - Model not loaded"}
        
        # Create features based on team names
        home_hash = hash(home_team) % 1000 / 1000.0
        away_hash = hash(away_team) % 1000 / 1000.0
        
        # Create 10 features for the model
        features = np.array([[
            home_hash, away_hash, abs(home_hash - away_hash),
            (home_hash + away_hash) / 2, home_hash * away_hash,
            home_hash ** 2, away_hash ** 2, (home_hash + away_hash) % 1,
            abs(home_hash - 0.5), abs(away_hash - 0.5)
        ]])
        
        # Make prediction
        prediction = model.predict(features)[0]
        
        # Calculate confidence
        try:
            decision_score = model.decision_function(features)[0]
            confidence = min(95, max(55, abs(decision_score) * 10 + 50))
        except:
            confidence = 75.0
        
        winner = home_team if prediction == 1 else away_team
        
        return {
            "winner": winner,
            "confidence": round(confidence, 1),
            "note": "Using trained model"
        }
        
    except Exception as e:
        return {"error": "Model Prediction Failure"}

@app.route('/')
def index():
    """Main page showing upcoming games"""
    games = get_upcoming_games()
    return render_template('index.html', games=games)

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """Serve static assets"""
    return send_from_directory('assets', filename)

@app.route('/predict/<game_id>')
def predict_game(game_id):
    """API endpoint to get prediction for a specific game"""
    games = get_upcoming_games()
    game = next((g for g in games if g['game_id'] == game_id), None)
    
    if not game:
        return jsonify({"error": "Game not found"})
    
    prediction = predict_game_winner(game['home_team'], game['away_team'])
    
    return jsonify({
        "game": game,
        "prediction": prediction
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)