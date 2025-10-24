
# UPI Fraud Prediction System

An ML-powered web app that analyzes UPI transaction details and predicts whether a transaction is likely to be fraudulent. Built with FastAPI for the backend, Jinja2 templates for the frontend, and scikit-learn models exported with joblib.

---

## Key Features

- Web form to submit transaction details (hour, day, month, year, amount, UPI number).
- Server-side inference using a pre-trained model (joblib).
- Multiple model training scripts included to compare algorithms (Random Forest, Logistic Regression, Decision Tree, SVM).

## Repository structure

- `app.py` — FastAPI application, serves UI and handles `/predict` POST requests.
- `4algos.py` — Training script that trains several models and saves them with joblib.
- `upi_fraud_dataset.csv` — Dataset used for training.
- `rf_model.pkl` (expected) — model file loaded by `app.py` at runtime (not committed here).
- `templates/` — Jinja2 HTML templates (`index.html`, `developers.html`).
- `static/` — static assets like `styles.css`.
- `requirements.txt` — Python dependencies.

## Prerequisites

- Python 3.8+ (3.10 recommended)
- pip

It is recommended to create and use a virtual environment.

## Installation

1. Create and activate a virtual environment (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

## Preparing / Training Models

The repository contains `4algos.py` which:

- Loads `upi_fraud_dataset.csv`.
- Encodes `upi_number`, scales features, trains multiple models, prints accuracies, and saves each model as `<model_name>_model.pkl` (e.g. `random_forest_model.pkl`).

To train models locally and save them, run:

```powershell
python 4algos.py
```

Note about model file name
-------------------------
`app.py` expects to load a model named `rf_model.pkl`:

```py
model = joblib.load("rf_model.pkl")
```

However, `4algos.py` saves models with names like `random_forest_model.pkl`. After training, either:

- Rename `random_forest_model.pkl` to `rf_model.pkl`, or
- Update `app.py` to load the exact model filename you trained (recommended for clarity).

Example rename (PowerShell):

```powershell
Rename-Item -Path .\random_forest_model.pkl -NewName rf_model.pkl
```

## Running the Web App (development)

Start the FastAPI server with uvicorn (from project root):

```powershell
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

Open a browser and go to:

http://127.0.0.1:8000

The main page provides a form to submit transaction data. The `/predict` endpoint accepts POSTed form fields (see the form in `templates/index.html`):

- `trans_hour` (0–23)
- `trans_day` (1–31)
- `trans_month` (1–12)
- `trans_year` (e.g. 2023)
- `trans_amount` (number)
- `upi_number` (string)

## API Endpoints

- `GET /` — Returns the form UI.
- `POST /predict` — Accepts form data and returns a rendered page with the prediction result.
- `GET /developers` — Developer credits page.

## Notes, caveats & next steps

- The current pipeline label-encodes `upi_number`. In production, you should carefully consider privacy and hashing/anonymization.
- Consider exposing a JSON API endpoint (instead of HTML form) for programmatic usage.
- Add a simple health check endpoint and logging for production deployments.
- Add unit tests for input validation and model inference.

## Dependencies

See `requirements.txt`. At a minimum the project needs:

- fastapi
- uvicorn
- joblib
- pandas
- jinja2
- python-multipart (for form parsing)

## Troubleshooting

- If you see an error loading the model, confirm the model filename matches what `app.py` expects (`rf_model.pkl`) or update `app.py`.
- Ensure your virtual environment is activated and requirements are installed.

## License & Authors

Include your preferred license here. If you'd like, I can add an `LICENSE` file.

Maintainers / Developers: See `templates/developers.html` for the project's developer credits.
