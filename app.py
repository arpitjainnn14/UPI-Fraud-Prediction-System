from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import joblib
import pandas as pd
import uvicorn
import os

app = FastAPI()

# Get the absolute path to the static directory
static_dir = os.path.join(os.path.dirname(__file__), "static")
templates_dir = os.path.join(os.path.dirname(__file__), "templates")

# Mount static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Setup templates
templates = Jinja2Templates(directory=templates_dir)

# Load the trained model with absolute path
model_path = os.path.join(os.path.dirname(__file__), "rf_model.pkl")
model = joblib.load(model_path)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/developers", response_class=HTMLResponse)
async def developers(request: Request):
    return templates.TemplateResponse("developers.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    trans_hour: int = Form(...),
    trans_day: int = Form(...),
    trans_month: int = Form(...),
    trans_year: int = Form(...),
    trans_amount: float = Form(...),
    upi_number: str = Form(...)
):
    # Create input data dictionary
    input_data = {
        "trans_hour": trans_hour,
        "trans_day": trans_day,
        "trans_month": trans_month,
        "trans_year": trans_year,
        "trans_amount": trans_amount,
        "upi_number": upi_number
    }

    # Create a DataFrame from input
    df = pd.DataFrame([input_data])

    # Predict with the model
    prediction = model.predict(df)[0]
    
    # Convert prediction to label
    result = "Fraud" if prediction == 1 else "Not Fraud"

    return templates.TemplateResponse("index.html", {"request": request, "result": result})

# For Vercel serverless deployment
# The app instance is automatically used by Vercel

# For local development only
if __name__ == '__main__':
    # Use PORT environment variable for Railway, default to 8000 for local
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
