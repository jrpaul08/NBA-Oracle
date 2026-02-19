# NBA Game Predictor Web App

A simple Flask web application that predicts NBA game winners using machine learning.

## Features

- 🏀 Real-time NBA games from ESPN API
- 🤖 AI predictions using trained RidgeClassifier model
- 📱 Responsive design
- ⚡ Fast predictions

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   python app.py
   ```

3. **Open your browser:**
   Go to `http://localhost:5002`

## How It Works

1. **Data Source**: Fetches upcoming NBA games from ESPN API
2. **Prediction**: Uses a trained RidgeClassifier model with team-based features
3. **Display**: Shows games in an interactive grid with prediction buttons

## Files

- `app.py` - Main Flask application
- `templates/index.html` - Web interface
- `requirements.txt` - Python dependencies
- `bball_game_winner_predictor_compatible.pkl` - Trained ML model

## Model Details

- **Algorithm**: RidgeClassifier
- **Features**: 10 team-based features derived from team names
- **Input**: Team names (home vs away)
- **Output**: Predicted winner with confidence score

## API Endpoints

- `GET /` - Main page with upcoming games
- `GET /predict/<game_id>` - Get prediction for specific game

## Notes

- Predictions are based on simplified team-based features
- For production use, integrate real team statistics
- Model uses fallback mock predictions if loading fails