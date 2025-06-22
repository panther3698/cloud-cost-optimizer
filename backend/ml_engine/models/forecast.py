import pandas as pd
from prophet import Prophet


def forecast_cost(data: pd.DataFrame) -> pd.DataFrame:
    """
    Forecasts cloud cost for the next 30 days using Facebook Prophet.

    Args:
        data (pd.DataFrame): DataFrame with columns:
            - 'date' (str or datetime): Dates in 'YYYY-MM-DD' format
            - 'cost' (float): Corresponding cost values

    Returns:
        pd.DataFrame: Forecast DataFrame with columns:
            - 'ds': Forecast dates
            - 'yhat': Predicted cost
            - 'yhat_lower': Lower bound
            - 'yhat_upper': Upper bound
    """
    # Validate columns
    if not {'date', 'cost'}.issubset(data.columns):
        raise ValueError("Input DataFrame must contain 'date' and 'cost' columns.")

    # Prepare data for Prophet
    df = data.copy()
    df['ds'] = pd.to_datetime(df['date'])
    df['y'] = df['cost']
    df = df[['ds', 'y']]

    # Train Prophet model
    model = Prophet(daily_seasonality=True)
    model.fit(df)

    # Create future dataframe for next 30 days
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
