import logging
import os
import pandas as pd
import sys

# Add the data loader directories to the Python path to avoid issues with the hyphenated 'data-ingestion' directory.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
data_ingestion_path = os.path.join(project_root, 'data-ingestion')
sys.path.insert(0, os.path.join(data_ingestion_path, 'aws'))
sys.path.insert(0, os.path.join(data_ingestion_path, 'azure'))
sys.path.insert(0, os.path.join(data_ingestion_path, 'gcp'))

from aws_loader import get_cost_and_usage as get_aws_cost
from azure_loader import get_daily_cost_by_resource_group as get_azure_cost
from gcp_loader import load_gcp_billing_data as get_gcp_cost

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_orchestration():
    """
    Orchestrates the process of fetching cost data from AWS, Azure, and GCP,
    and merges them into a single DataFrame.

    Returns:
        pandas.DataFrame: A unified DataFrame containing cost data from all
                          three cloud providers. The DataFrame has the columns:
                          'date', 'provider', 'service', 'cost'.
                          Returns an empty DataFrame if no data can be fetched.
    """
    all_dfs = []

    # 1. Fetch AWS Data
    logging.info("Attempting to fetch AWS cost data...")
    try:
        aws_df = get_aws_cost()
        if not aws_df.empty:
            aws_df['provider'] = 'aws'
            all_dfs.append(aws_df)
            logging.info(f"Successfully fetched {len(aws_df)} rows of AWS cost data.")
        else:
            logging.warning("AWS cost data is empty. No data fetched or credentials problem.")
    except Exception as e:
        logging.error(f"Failed to fetch AWS cost data: {e}")

    # 2. Fetch Azure Data
    logging.info("Attempting to fetch Azure cost data...")
    azure_sub_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    if azure_sub_id:
        try:
            azure_df = get_azure_cost(azure_sub_id)
            if not azure_df.empty:
                azure_df = azure_df.rename(columns={'resource_group': 'service'})
                azure_df['provider'] = 'azure'
                all_dfs.append(azure_df)
                logging.info(f"Successfully fetched {len(azure_df)} rows of Azure cost data.")
            else:
                logging.warning("Azure cost data is empty. No data fetched or credentials/permissions problem.")
        except Exception as e:
            logging.error(f"Failed to fetch Azure cost data: {e}")
    else:
        logging.warning("AZURE_SUBSCRIPTION_ID environment variable not set. Skipping Azure cost data.")

    # 3. Fetch GCP Data
    logging.info("Attempting to fetch GCP cost data...")
    gcp_table_name = os.environ.get("GCP_BILLING_EXPORT_TABLE")
    if gcp_table_name:
        try:
            gcp_df = get_gcp_cost(gcp_table_name)
            if not gcp_df.empty:
                gcp_df['provider'] = 'gcp'
                all_dfs.append(gcp_df)
                logging.info(f"Successfully fetched {len(gcp_df)} rows of GCP cost data.")
            else:
                logging.warning("GCP cost data is empty. No data fetched or credentials/permissions problem.")
        except Exception as e:
            logging.error(f"Failed to fetch GCP cost data: {e}")
    else:
        logging.warning("GCP_BILLING_EXPORT_TABLE environment variable not set. Skipping GCP cost data.")

    # 4. Merge DataFrames
    if not all_dfs:
        logging.warning("No data was fetched from any cloud provider. Returning empty DataFrame.")
        return pd.DataFrame(columns=['date', 'provider', 'service', 'cost'])

    merged_df = pd.concat(all_dfs, ignore_index=True)
    
    # Standardize date column to datetime objects
    merged_df['date'] = pd.to_datetime(merged_df['date'])

    # Ensure consistent column order
    final_columns = ['date', 'provider', 'service', 'cost']
    merged_df = merged_df[final_columns]

    logging.info(f"Successfully merged data from {len(all_dfs)} providers.")
    logging.info(f"Total rows in merged DataFrame: {len(merged_df)}")
    
    return merged_df

if __name__ == '__main__':
    logging.info("Starting cloud cost orchestration script.")
    
    # For demonstration, you might need to set environment variables like this:
    # os.environ['AZURE_SUBSCRIPTION_ID'] = 'your-subscription-id'
    # os.environ['GCP_BILLING_EXPORT_TABLE'] = 'your-project.your_dataset.your_table'
    
    final_cost_data = run_orchestration()

    if not final_cost_data.empty:
        logging.info("Orchestration complete. Displaying head of the final DataFrame:")
        print(final_cost_data.head())
        logging.info("Displaying tail of the final DataFrame:")
        print(final_cost_data.tail())
        logging.info("DataFrame Info:")
        final_cost_data.info()
    else:
        logging.warning("Orchestration resulted in an empty DataFrame. No data to display.")

    logging.info("Cloud cost orchestration script finished.")
