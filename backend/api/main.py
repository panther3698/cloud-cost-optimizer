import pandas as pd
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List

# Adjust imports to match your project structure
from backend.ml_engine.models.forecast import forecast_cost
from backend.ml_engine.models.anomaly import detect_anomalies

# App initialization
app = FastAPI(
    title="Cloud Cost Optimizer API",
    description="API for forecasting cloud costs and detecting anomalies.",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Pydantic models for request bodies
class CostData(BaseModel):
    date: str
    cost: float

class CostDataPayload(BaseModel):
    data: List[CostData]

# Generic error handler
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"An unexpected error occurred: {exc}"},
    )

# API Endpoints
@app.get("/")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

@app.post("/forecast")
def get_forecast(payload: CostDataPayload):
    """
    Accepts cost data and returns a 30-day forecast.
    """
    try:
        # Convert Pydantic models to a pandas DataFrame
        df = pd.DataFrame([item.dict() for item in payload.data])
        if df.empty:
            raise HTTPException(status_code=400, detail="No data provided.")
        
        # Get forecast
        forecast_df = forecast_cost(df)
        
        # Convert forecast DataFrame to JSON
        return forecast_df.to_dict(orient="records")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during forecasting: {e}")


@app.post("/anomaly")
def get_anomalies(payload: CostDataPayload):
    """
    Accepts cost data and returns anomaly detection results.
    """
    try:
        # Convert Pydantic models to a pandas DataFrame
        df = pd.DataFrame([item.dict() for item in payload.data])
        if df.empty:
            raise HTTPException(status_code=400, detail="No data provided.")

        # Detect anomalies
        anomaly_df = detect_anomalies(df)

        # Convert anomaly DataFrame to JSON
        return anomaly_df.to_dict(orient="records")
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during anomaly detection: {e}")
