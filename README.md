# NBA Game Predictor 🏀

An end-to-end machine learning project that predicts NBA game winners. Includes data scraping, model training, and a Flask web application.

## Features

- 📊 Web scraping pipeline to collect NBA game data from ESPN
- 🔬 Data parsing and feature engineering notebooks
- 🤖 ML model training using RidgeClassifier
- 🌐 Flask web app with real-time predictions

## Project Structure

```
├── Notebooks/
│   ├── get_live_data.ipynb    # Web scraping with Playwright
│   ├── parse_data.ipynb       # Data parsing and cleaning
│   ├── predict_tutorial.ipynb # Model training walkthrough
│   └── predict_live.ipynb     # Live prediction notebook
├── app.py                     # Flask web application
├── templates/index.html       # Web interface
├── nba_games.csv             # Processed game data
├── *.pkl                      # Trained models
└── requirements.txt
```

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the web app:**
   ```bash
   python app.py
   ```

3. **Open browser:** http://localhost:5002

## Notebooks

| Notebook | Description |
|----------|-------------|
| `get_live_data.ipynb` | Scrapes NBA box scores using Playwright |
| `parse_data.ipynb` | Parses HTML and creates structured dataset |
| `predict_tutorial.ipynb` | Trains and evaluates the ML model |
| `predict_live.ipynb` | Makes predictions on upcoming games |

## Tech Stack

- **Scraping:** Playwright, BeautifulSoup
- **Data:** Pandas, NumPy
- **ML:** scikit-learn (RidgeClassifier)
- **Web:** Flask
- **API:** ESPN Scoreboard API

