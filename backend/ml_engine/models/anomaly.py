import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(data: pd.DataFrame) -> pd.DataFrame:
    """
    Uses IsolationForest to detect anomalies in cloud cost data.

    Args:
        data (pd.DataFrame): DataFrame with columns 'date' and 'cost'

    Returns:
        pd.DataFrame: Original data with 'is_anomaly' column added (True if anomaly)
    """
    df = data.copy()

    # Validate required columns
    if not {'date', 'cost'}.issubset(df.columns):
        raise ValueError("Input DataFrame must contain 'date' and 'cost' columns.")

    # Fit IsolationForest on cost column
    model = IsolationForest(contamination=0.05, random_state=42)
    df['anomaly_score'] = model.fit_predict(df[['cost']])
    df['is_anomaly'] = df['anomaly_score'] == -1

    # Drop intermediate score column
    return df.drop(columns=['anomaly_score'])
