import json
import pandas as pd
from backend.ml_engine.models.forecast import forecast_cost
from backend.ml_engine.models.anomaly import detect_anomalies
from llm_engine.llm_chat import chat_with_llm

def generate_monthly_cost_summary(provider='aws', **kwargs):
    """
    Generate a monthly cost summary report from forecast + actuals for a given cloud provider:
    - Top 5 services
    - Anomalies found
    - Recommendations (LLM-generated)
    Return as JSON

    Args:
        provider (str): 'aws', 'azure', or 'gcp'.
        kwargs: Additional arguments for the loader (e.g., subscription_id for Azure, table_name for GCP).
    """
    # Import the correct loader based on provider
    try:
        if provider == 'aws':
            try:
                from data_ingestion.aws import aws_loader  # type: ignore[import]
            except ImportError:
                from ..data_ingestion.aws import aws_loader  # type: ignore[import]
            actuals = aws_loader.get_cost_and_usage()
        elif provider == 'azure':
            try:
                from data_ingestion.azure import azure_loader  # type: ignore[import]
            except ImportError:
                from ..data_ingestion.azure import azure_loader  # type: ignore[import]
            subscription_id = kwargs.get('subscription_id')
            actuals = azure_loader.get_daily_cost_by_resource_group(subscription_id)
            # Rename for consistency
            if not actuals.empty:
                actuals = actuals.rename(columns={"resource_group": "service"})
        elif provider == 'gcp':
            try:
                from data_ingestion.gcp import gcp_loader  # type: ignore[import]
            except ImportError:
                from ..data_ingestion.gcp import gcp_loader  # type: ignore[import]
            table_name = kwargs.get('table_name')
            actuals = gcp_loader.load_gcp_billing_data(table_name)
        else:
            return json.dumps({"error": f"Unknown provider: {provider}"})
    except Exception as e:
        return json.dumps({"error": f"Could not load cost data for {provider}: {e}"})

    if actuals.empty:
        return json.dumps({"error": "No cost data available."})

    # 2. Forecast costs (optional, not used in top 5/anomaly but could be included)
    # Group by date for total cost forecast
    daily_costs = actuals.groupby('date').agg({'cost': 'sum'}).reset_index()
    forecast_df = forecast_cost(daily_costs.rename(columns={'date': 'date', 'cost': 'cost'}))

    # 3. Top 5 services by total cost
    top_services_df = (
        actuals.groupby('service', as_index=False)['cost']
        .sum()
        .sort_values(by='cost', ascending=False)
        .head(5)
    )
    top_services = top_services_df.to_dict(orient='records')  # type: ignore[attr-defined]

    # 4. Anomaly detection
    anomalies_df = detect_anomalies(
        actuals[['date', 'cost']].groupby('date', as_index=False).sum()
    )
    # Ensure anomalies_df is a DataFrame before calling to_dict
    if hasattr(anomalies_df, 'to_dict'):
        anomalies = anomalies_df[anomalies_df['is_anomaly'] == True].to_dict(orient='records')  # type: ignore[attr-defined]
    else:
        anomalies = []

    # 5. LLM Recommendations
    # Summarize cost data for LLM (e.g., top services, total cost)
    summary_str = f"Top services: {top_services}\nTotal cost: {actuals['cost'].sum():.2f}"
    try:
        recommendations = chat_with_llm(
            question_type="recommend_savings",
            cost_data=summary_str,
            persona="FinOps",
            use_azure=True
        )
    except Exception as e:
        recommendations = f"LLM error: {e}"

    # 6. Assemble report
    report = {
        "top_services": top_services,
        "anomalies": anomalies,
        "recommendations": recommendations,
    }
    return json.dumps(report, default=str, indent=2)
