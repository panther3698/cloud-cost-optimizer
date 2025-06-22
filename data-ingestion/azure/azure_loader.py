import os
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional

from azure.identity import DefaultAzureCredential
from azure.mgmt.costmanagement import CostManagementClient
from azure.core.exceptions import ClientAuthenticationError, HttpResponseError

def get_daily_cost_by_resource_group(
    subscription_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> pd.DataFrame:
    """
    Fetches daily cost by resource group from Azure Cost Management.

    Args:
        subscription_id: Your Azure subscription ID.
        start_date: The start date for the query in 'YYYY-MM-DD' format. 
                      Defaults to 30 days ago.
        end_date: The end date for the query in 'YYYY-MM-DD' format. 
                  Defaults to today.

    Returns:
        A pandas DataFrame with columns: 'date', 'resource_group', 'cost'.
    """
    if start_date is None:
        start_date = (datetime.utcnow() - timedelta(days=30)).strftime('%Y-%m-%d')
    if end_date is None:
        end_date = datetime.utcnow().strftime('%Y-%m-%d')

    try:
        credential = DefaultAzureCredential()
        cost_management_client = CostManagementClient(credential)

        scope = f"/subscriptions/{subscription_id}"
        
        parameters = {
            "type": "ActualCost",
            "timeframe": "Custom",
            "time_period": {
                "from": f"{start_date}T00:00:00+00:00",
                "to": f"{end_date}T23:59:59+00:00"
            },
            "dataset": {
                "granularity": "Daily",
                "aggregation": {
                    "totalCost": {
                        "name": "Cost",
                        "function": "Sum"
                    }
                },
                "grouping": [
                    {
                        "type": "Dimension",
                        "name": "ResourceGroupName"
                    }
                ]
            }
        }

        result = cost_management_client.query.usage(scope, parameters)
        
        columns = [col.name for col in result.columns]
        data = result.rows

        df = pd.DataFrame(data, columns=columns)

        if df.empty:
            return pd.DataFrame(columns=['date', 'resource_group', 'cost'])
            
        df = df.rename(columns={
            'UsageDate': 'date',
            'ResourceGroupName': 'resource_group',
            'Cost': 'cost'
        })

        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d').dt.date
        df['cost'] = df['cost'].astype(float)
        
        return df[['date', 'resource_group', 'cost']]

    except ClientAuthenticationError:
        print("Authentication failed. Please check your Azure credentials.")
        print("You may need to run 'az login' or set environment variables.")
        return pd.DataFrame()
    except HttpResponseError as e:
        print(f"An HTTP error occurred: {e.message}")
        return pd.DataFrame()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return pd.DataFrame()

if __name__ == '__main__':
    # Example usage:
    # Make sure to set the AZURE_SUBSCRIPTION_ID environment variable
    # or replace os.environ.get("AZURE_SUBSCRIPTION_ID") with your subscription ID.
    sub_id = os.environ.get("AZURE_SUBSCRIPTION_ID")

    if not sub_id:
        print("Please set the AZURE_SUBSCRIPTION_ID environment variable.")
    else:
        print(f"Fetching costs for subscription: {sub_id}")
        # Fetch costs for the last 7 days
        seven_days_ago = (datetime.utcnow() - timedelta(days=7)).strftime('%Y-%m-%d')
        today = datetime.utcnow().strftime('%Y-%m-%d')
        
        cost_df = get_daily_cost_by_resource_group(sub_id, start_date=seven_days_ago, end_date=today)
        
        if not cost_df.empty:
            print("Successfully fetched daily costs by resource group:")
            print(cost_df.to_string())
        else:
            print("Could not fetch cost data.")
