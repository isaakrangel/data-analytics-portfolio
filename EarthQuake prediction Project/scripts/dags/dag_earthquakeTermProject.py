from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
import os
from airflow.operators.bash import BashOperator
from airflow.providers.ftp.hooks.ftp import FTPSHook
import ssl
from ftplib import FTP_TLS
from airflow.hooks.base import BaseHook


# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


# ---------------------------------------------------------
# 1. Extraction Logic
# ---------------------------------------------------------
def extract_cleaned_data():
    import glob
    import pandas as pd
    
    # Load the clean data CSVs - data from 2010-2026
    # Note: Ensure the path is accessible to the Airflow worker
    files = glob.glob("/opt/airflow/project_data/data/cleaned/*.csv")
    
    if not files:
        raise ValueError("No CSV files found in the specified directory.")
        
    # Loop through them, read them, and stitch them together
    df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    
    # Save to an intermediate staging location for the next task
    staging_path = '/tmp/extracted_earthquake_data.csv'
    df.to_csv(staging_path, index=False)
    print(f"Successfully extracted {len(df)} rows and saved to {staging_path}.")

# ---------------------------------------------------------
# 2. Transformation Logic
# ---------------------------------------------------------
def process_transform():
    import pandas as pd
    import numpy as np
    
    # Read the data saved by the previous task
    df = pd.read_csv('/tmp/extracted_earthquake_data.csv')

    # Bins for magnitude (Low, Light, Moderate, Strong)
    bins = [0, 4, 5.0, 6.0, np.inf]
    labels = ['0', '1', '2', '3']
    df['mag_bin'] = pd.cut(df['mag'], bins=bins, labels=labels, right=False)
    df['mag_bin'] = df['mag_bin'].astype(int)

    # Convert the time column to a datetime object, handling mixed ISO8601 formats
    df['time'] = pd.to_datetime(df['time'], format='ISO8601')
    df['year'] = df['time'].dt.year
    df['month'] = df['time'].dt.month
    df['hour'] = df['time'].dt.hour
    df['day'] = df['time'].dt.day

    # Sorted by time and calculate differences in minutes
    df = df.sort_values('time')
    df['time_diff_minutes'] = df['time'].diff().dt.total_seconds() / 60
    df['time_diff_minutes'] = df['time_diff_minutes'].fillna(0)

    # Drop unneeded columns
    columns_to_drop = ['time', 'net', 'id', 'updated', 'place', 'type', 'status', 'locationSource', 'magSource', 'date']
    df.drop(columns=[col for col in columns_to_drop if col in df.columns], axis=1, inplace=True)

    # Fill numerical columns with 0
    numerical_cols = ['nst', 'gap', 'dmin', 'rms', 'horizontalError', 'depthError', 'magError', 'magNst']
    for col in numerical_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0).astype(int)

    # Use structural modes for missing temporal dimensions
    for temporal_col in ['year', 'month', 'day', 'hour']:
        if temporal_col in df.columns:
            df[temporal_col] = df[temporal_col].fillna(df[temporal_col].mode()[0]).astype(int)

    # Dynamic encoding setup for multi-stage categorical 'magType'
    if 'magType' in df.columns:
        df = pd.get_dummies(df, columns=['magType'], drop_first=True, dtype=int)
    else:
        magtype_cols = [col for col in df.columns if col.startswith('magType_')]
        df[magtype_cols] = df[magtype_cols].fillna(0).astype(int)

    # Fill any structural missing fields across remaining environmental/weather sensor metrics
    df = df.fillna(0)

    # Save transformed data
    transformed_path = '/tmp/transformed_earthquake_data.csv'
    df.to_csv(transformed_path, index=False)
    print(f"Data transformed successfully. Missing values remaining: {df.isnull().sum().sum()}")

# ---------------------------------------------------------
# 3. Load Logic
# ---------------------------------------------------------
def load_to_csv():
    import pandas as pd
    
    # Read the transformed data
    df = pd.read_csv('/tmp/transformed_earthquake_data.csv')
    
    # Define the final model-ready destination path
    final_output_dir = "/opt/airflow/project_data/data/reports/"
    os.makedirs(final_output_dir, exist_ok=True)
    final_path = os.path.join(final_output_dir, "earthquake_model_ready.csv")
    
    # Save the final dataset
    df.to_csv(final_path, index=False)
    print(f"Pipeline complete! Final dataset loaded to: {final_path}")

# ---------------------------------------------------------
# 4. Prediction & Forecast Logic
# ---------------------------------------------------------
def generate_forecast():
    import pandas as pd
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler
    from sklearn.feature_selection import SelectFromModel
    from sklearn.pipeline import Pipeline
    import os

    # Read the transformed data
    df = pd.read_csv('/tmp/transformed_earthquake_data.csv')
    
    # Isolate feature vectors from the explicit labels
    X = df.drop(['mag_bin', 'mag'], axis=1, errors='ignore')
    y = df['mag_bin']

    # Initialize balanced random forest classifiers
    rfc_balanced = RandomForestClassifier(
        n_estimators=200, 
        max_depth=8, 
        class_weight='balanced', 
        random_state=42, 
        n_jobs=-1
    )
    
    selector = SelectFromModel(
        RandomForestClassifier(n_estimators=100, max_depth=4, class_weight='balanced', random_state=42),
        threshold="median"
    )

    # Define full pipeline structure
    pipeline = Pipeline(steps=[
        ('scaler', StandardScaler()),    
        ('selector', selector),
        ('classifier', rfc_balanced)
    ]) 

    # Train optimal model chain
    pipeline.fit(X, y)

    # Define target timeline (10 days starting from 2026-06-24)
    forecast_dates = pd.date_range(start='2026-06-24', periods=10, freq='D')
    #forecast_dates = pd.date_range(start='2026-07-28', periods=10, freq='D')
    
    # Extract feature baselines
    means = X.mean()
    stds = X.std()

    # Construct dynamic daily feature records globally
    future_records = []
    for current_date in forecast_dates:
        simulated_record = np.random.normal(loc=means, scale=stds)
        record = pd.Series(simulated_record, index=X.columns)
        
        record['latitude'] = np.clip(record['latitude'], -90.0, 90.0)
        record['longitude'] = np.clip(record['longitude'], -180.0, 180.0)
        record['year'] = current_date.year
        record['month'] = current_date.month
        record['day'] = current_date.day
        record['hour'] = np.random.randint(0, 24)

        non_negative_cols = [
            'nst', 'gap', 'dmin', 'precipitation', 
            'soil_moisture_0_7cm', 'soil_moisture_100_255cm', 
            'depth', 'horizontalError'
        ]
        for col in non_negative_cols:
            if col in record.index:
                record[col] = max(0, record[col])

        future_records.append(record)

    df_future = pd.DataFrame(future_records)[X.columns]

    # Predict category probabilities and choices
    future_probabilities = pipeline.predict_proba(df_future)
    future_predictions = pipeline.predict(df_future)

    class_mapping = {0: 'Low', 1: 'Light', 2: 'Moderate', 3: 'Strong'}

    # Build summary forecast table
    df_forecast_range = pd.DataFrame({
        'Date': [d.strftime('%Y-%m-%d') for d in forecast_dates],
        'Lat_Center': df_future['latitude'].round(4),
        'Lon_Center': df_future['longitude'].round(4),
        'Predicted_Category': [class_mapping[pred] for pred in future_predictions],
        'Low_%': (future_probabilities[:, 0] * 100).round(2),
        'Light_%': (future_probabilities[:, 1] * 100).round(2),
        'Moderate_%': (future_probabilities[:, 2] * 100).round(2),
        'Strong_%': (future_probabilities[:, 3] * 100).round(2)
    })

    # Save output using the absolute path mapped in Docker
    final_output_dir = "/opt/airflow/project_data/data/reports/"
    os.makedirs(final_output_dir, exist_ok=True)
    forecast_path = os.path.join(final_output_dir, "10_day_global_forecast.csv")
    
    df_forecast_range.to_csv(forecast_path, index=False)
    print(f"Forecast successfully generated and saved to: {forecast_path}")

### put in a FTP
def upload_forecast_to_ftp(local_filepath, remote_filepath):
    # 1. Fetch credentials securely from the Airflow UI Connection
    conn = BaseHook.get_connection('neonet_ftps_conn')
    
    # 2. Create an SSL context that ignores the hostname mismatch
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    # 3. Connect manually using Python's standard ftplib
    print(f"Connecting to {conn.host}...")
    ftps = FTP_TLS(host=conn.host, context=context)
    ftps.login(user=conn.login, passwd=conn.password)
    
    # 4. Force a secure data connection (Required for Explicit FTPS)
    ftps.prot_p() 
    
    # 5. Upload the file
    print(f"Uploading {local_filepath}...")
    with open(local_filepath, 'rb') as file:
        ftps.storbinary(f'STOR {remote_filepath}', file)
        
    ftps.quit()
    print(f"Successfully uploaded {local_filepath} to {remote_filepath}")
### end

# ---------------------------------------------------------
# 5. DAG Definition
# ---------------------------------------------------------
with DAG(
    'earthquake_data_pipeline',
    default_args=default_args,
    schedule='@daily',
    catchup=False,
    tags=['project']
) as dag:

    task_extract_cleaned_data = PythonOperator(
        task_id='extract_cleaned_data',
        python_callable=extract_cleaned_data,
    )

    task_process_transform = PythonOperator(
        task_id='process_transform',
        python_callable=process_transform,
    )

    task_load_to_csv = PythonOperator(
        task_id='load_to_csv',
        python_callable=load_to_csv,
    )
    
    # Register the new prediction task
    task_generate_forecast = PythonOperator(
        task_id='generate_forecast',
        python_callable=generate_forecast,
    )

    # upload to FTP
    upload_forecast_task = PythonOperator(
        task_id='upload_forecast_ftp',
        python_callable=upload_forecast_to_ftp,
        op_kwargs={
            # Replace these with the actual paths in your Airflow environment and FTP server
            'local_filepath': '/opt/airflow/project_data/data/reports/10_day_global_forecast.csv', 
            'remote_filepath': '10_day_global_forecast.csv' 
        }
    )

    # Set the updated execution order dependencies
    task_extract_cleaned_data >> task_process_transform >> task_load_to_csv >> task_generate_forecast >> upload_forecast_task