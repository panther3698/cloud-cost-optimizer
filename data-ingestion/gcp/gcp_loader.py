import os
import pandas as pd
from google.cloud import bigquery
from google.api_core import exceptions

def load_gcp_billing_data(table_name: str) -> pd.DataFrame:
    """
    Loads cost data from a GCP billing export table in BigQuery.

    This function queries a BigQuery table containing GCP billing data,
    extracts the date, service description, and cost, and returns it
    as a pandas DataFrame. It uses Application Default Credentials for
    authentication.

    Args:
        table_name: The fully qualified BigQuery table name in the format
                    `project.dataset.table`.

    Returns:
        A pandas DataFrame with the following columns:
        - date: The date of the cost.
        - service: The description of the service.
        - cost: The cost associated with the service on that date.
        Returns an empty DataFrame if an error occurs.

    Raises:
        ValueError: If the table_name is not in the expected format.
    """
    if len(table_name.split('.')) != 3:
        raise ValueError("table_name must be in the format `project.dataset.table`")

    try:
        # Initialize the BigQuery client.
        # Application Default Credentials are used automatically.
        client = bigquery.Client()

        # Construct the SQL query to fetch billing data.
        # This query aggregates costs by date and service.
        query = f"""
            SELECT
                CAST(usage_start_time AS DATE) AS date,
                service.description AS service,
                SUM(cost) AS cost
            FROM
                `{table_name}`
            GROUP BY
                1, 2
            ORDER BY
                date, service
        """

        print(f"Executing query on table: {table_name}")
        # Execute the query and load the results into a pandas DataFrame.
        df = client.query(query).to_dataframe()

        return df

    except exceptions.Forbidden as e:
        print(f"Permission denied to BigQuery table {table_name}.")
        print("Please ensure your Application Default Credentials have the necessary IAM permissions (e.g., BigQuery User).")
        print(f"Error: {e}")
        return pd.DataFrame()

    except exceptions.NotFound as e:
        print(f"BigQuery table {table_name} not found.")
        print(f"Error: {e}")
        return pd.DataFrame()
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return pd.DataFrame()

if __name__ == '__main__':
    # Example usage:
    # Before running, authenticate with Google Cloud:
    # 1. Install gcloud CLI: https://cloud.google.com/sdk/docs/install
    # 2. Run `gcloud auth application-default login` in your terminal.
    
    # IMPORTANT: Replace with your actual project, dataset, and table name.
    # You can also set this as an environment variable.
    bq_table = os.environ.get("GCP_BILLING_EXPORT_TABLE") 

    if bq_table:
        print(f"Loading data from BigQuery table: {bq_table}")
        cost_data = load_gcp_billing_data(bq_table)
        if not cost_data.empty:
            print("\nSuccessfully loaded billing data.")
            print(cost_data.head())
            print(f"\nTotal rows: {len(cost_data)}")
    else:
        print("\nTo run this module directly, set the 'GCP_BILLING_EXPORT_TABLE' environment variable.")
        print("Example for PowerShell:")
        print("$env:GCP_BILLING_EXPORT_TABLE='your-gcp-project.your_dataset.your_billing_table'")
        print("Example for bash/zsh:")
        print("export GCP_BILLING_EXPORT_TABLE='your-gcp-project.your_dataset.your_billing_table'")
