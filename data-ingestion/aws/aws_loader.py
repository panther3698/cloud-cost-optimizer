import boto3
import pandas as pd
from datetime import datetime, timedelta
from botocore.exceptions import NoCredentialsError

def get_cost_and_usage():
    """
    Queries AWS Cost Explorer for daily cost data, grouped by service, for the last 30 days.

    The function retrieves unblended costs and groups them by service on a daily basis.
    It requires AWS credentials to be configured in the environment.

    Returns:
        pandas.DataFrame: A DataFrame with the following columns:
                          'date' (object, YYYY-MM-DD),
                          'service' (str),
                          'cost' (float).
                          Returns an empty DataFrame if AWS credentials are not found or
                          if there is no cost data.
    """
    try:
        # Cost Explorer is a global service, but a region must be specified.
        ce_client = boto3.client('ce', region_name='us-east-1')
    except NoCredentialsError:
        print("Error: AWS credentials not found. Please configure your credentials (e.g., via `aws configure`).")
        return pd.DataFrame(columns=['date', 'service', 'cost'])

    # Set the time period for the last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')

    results = []
    token = None

    while True:
        if token:
            kwargs = {'NextPageToken': token}
        else:
            kwargs = {}

        try:
            response = ce_client.get_cost_and_usage(
                TimePeriod={
                    'Start': start_str,
                    'End': end_str
                },
                Granularity='DAILY',
                Metrics=['UnblendedCost'],
                GroupBy=[
                    {
                        'Type': 'DIMENSION',
                        'Key': 'SERVICE'
                    }
                ],
                **kwargs
            )
        except Exception as e:
            print(f"An error occurred while fetching cost data: {e}")
            return pd.DataFrame(columns=['date', 'service', 'cost'])


        for result_by_time in response.get('ResultsByTime', []):
            for group in result_by_time.get('Groups', []):
                results.append({
                    'date': result_by_time['TimePeriod']['Start'],
                    'service': group['Keys'][0],
                    'cost': float(group['Metrics']['UnblendedCost']['Amount'])
                })

        token = response.get('NextPageToken')
        if not token:
            break

    if not results:
        return pd.DataFrame(columns=['date', 'service', 'cost'])

    df = pd.DataFrame(results)
    df['date'] = pd.to_datetime(df['date']).dt.date
    return df

if __name__ == '__main__':
    print("Fetching AWS cost data for the last 30 days...")
    cost_data = get_cost_and_usage()
    if not cost_data.empty:
        print("Successfully fetched cost data.")
        print(cost_data.head())
    else:
        print("Could not fetch cost data. Please check your AWS credentials and permissions, or there might be no cost data in the specified period.")
