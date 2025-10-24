from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import joblib
import pandas as pd
import uvicorn

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Load the trained model
model = joblib.load("rf_model.pkl")

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

if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
