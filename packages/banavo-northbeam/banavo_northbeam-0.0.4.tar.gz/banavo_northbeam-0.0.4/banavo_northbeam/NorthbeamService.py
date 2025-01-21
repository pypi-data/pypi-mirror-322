import os
import time
from datetime import datetime, timedelta
import requests
import pandas as pd
import numpy as np
from pymongo import MongoClient
import boto3
import sys
import json
import traceback
import json
import traceback
from urllib.parse import urlparse
import pytz
from pytz import timezone


class NorthbeamService:
    def __init__(self, northbeam_api_key, northbeam_data_client_id, collection_name, dbname, mongo_connection_url, slack_client, tjc_configuration_s3_path, job_name, use_production=False):

        self.northbeam_api_key = northbeam_api_key
        self.nortbeam_data_client_id = northbeam_data_client_id
        self.collection_name = collection_name
        self.dbname = dbname
        self.mongo_connection_url = mongo_connection_url
        self.tjc_configuration_s3_path = tjc_configuration_s3_path
        self.job_name = job_name
        self.use_production = use_production

        print('instantiating client')
        self.lambda_client = boto3.client('lambda', region_name='us-east-1') # invoke the function in us-east-1
        self.s3_client = boto3.client("s3")
        self.slack_client = slack_client
        print('done with init')

    def notify_on_slack(self, status, message, error="", stackTrace="",client=""):
        print('notifying on slack')
        payload = json.dumps({
            'message': message,
            'status': status,
            'errorLogs': error,
            'stackTrace': stackTrace,
            'client':client
        })
        # trigger the lambda function to send a slack notification about the status of the glue job
        response = self.lambda_client.invoke(
            FunctionName='trigger-slack-notification', 
            InvocationType='RequestResponse',      # Synchronous invocation
            Payload=payload
        )
        print('done notifying')
        return response['Payload'].read()   # returns the output of the lambda FunctionName

    def get_export_status(self, export_id, max_retries=5, delay=10): 
        print('getting export status')
        url = f"https://api.northbeam.io/v1/exports/data-export/result/{export_id}"
        headers = {
            "accept": "application/json",
            "Authorization": self.northbeam_api_key,
            "Data-Client-ID": self.nortbeam_data_client_id
        }
        for attempt in range(max_retries):
            export_response = requests.get(url, headers=headers)
            export_result = export_response.json()
            export_status = export_result.get('status')

            if export_status == 'SUCCESS':
                result_url = export_result.get('result')[0]
                return result_url
            elif export_status != 'PENDING':
                raise Exception(f"Export status is not 'success': {export_status}")
            if attempt < max_retries - 1:
                time.sleep(delay)
        raise Exception("Max retries exceeded, export status not 'success'")

    def upload_file_to_s3(self, bucket_name, folder_name,file_name, file_path):
        print('uploading file to s3')
        s3_client = boto3.client(
            's3',
            region_name='ap-south-1'
        )
        s3_key = f"{folder_name}/{file_name}"
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f'File uploaded to s3://{bucket_name}/{s3_key}')
        return
    
    def transfer_to_mongodb(self, csv_file_path, mongodb_connection_string, dbname, collection_name):
        print('transferring to mongo')
        client = MongoClient(mongodb_connection_string)
        db = client[dbname]
        collection = db[collection_name]
        collection.drop() # getting rid of the collection
        collection = db[collection_name]
        df = pd.read_csv(csv_file_path, parse_dates= ['date'])
        df.replace({np.nan: None}, inplace=True)
        print(df['date'].head(10))
        print(df.dtypes)
        df['date'] = pd.to_datetime(df['date']).dt.tz_localize('US/Central').dt.tz_convert('UTC') # will likely have to change this since data might be in GMT time zone
        data = df.to_dict(orient='records')
        collection.insert_many(data)
        client.close()
        print('done with transfer')
        return
    
    def run_northbeam_data_pipeline(self):
        print('running northbeam pipeline')
        try:
            # Northbeam API call for export
            url = "https://api.northbeam.io/v1/exports/breakdowns"
            headers = {
                "accept": "application/json",
                "Authorization": self.northbeam_api_key,
                "Data-Client-ID": self.nortbeam_data_client_id
            }
            response = requests.get(url, headers=headers)
            breakdown_result = response.json()
            filtered_break_downs = [breakdown for breakdown in breakdown_result.get('breakdowns') if breakdown.get('key') == 'Platform (Northbeam)']
    
            print("breakdown>>", filtered_break_downs)

            #today = datetime.utcnow()
            tz = pytz.timezone(timezone)
            today = datetime.now(tz)
            print('BST TIME NOW:', today)

            two_years_ago = today - timedelta(days=2*365)
            four_years_ago = today - timedelta(days=4*365)

            gmt_start_time = self.convert_to_gmt(two_years_ago)
            gmt_end_time = self.convert_to_gmt(today)
    
            start_time = gmt_start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            end_time = gmt_end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

            payload = {
                "level": "platform",
                "time_granularity": "DAILY",
                # "period_type": "YESTERDAY",
                "period_type": "FIXED",
                "period_options": {
                    "period_starting_at": start_time,
                    "period_ending_at": end_time
                },
                "breakdowns": filtered_break_downs,
                "options": {
                    "export_aggregation": "DATE",
                    "remove_zero_spend": False,
                    "aggregate_data": True
                },
                "attribution_options": {
                    "attribution_models": ["northbeam_custom__va", "northbeam_custom", "last_touch","last_touch_non_direct","first_touch","linear"],
                    "accounting_modes": ["accrual", "cash"],
                    "attribution_windows": ["1", "3","7","14","30","60","90"],
                },
                "metrics": [
                    {"id": "spend"},
                    {"id": "cac"},
                    {"id": "cacFt"},
                    {"id": "cacRtn"},
                    {"id": "ctr"},
                    {"id": "ecr"},
                    {"id": "revAttributed"},
                    {"id": "revAttributedFt"},
                    {"id": "revAttributedRtn"},
                    {"id": "roas"},
                    {"id": "roasFt"},
                    {"id": "roasRtn"},
                    {"id": "txns"},
                    {"id": "txnsFt"},
                    {"id": "txnsRtn"},
                    {"id": "visits"},
                    {"id": "newVisits"},
                    {"id": "newVisitsPercentage"},
                    {"id": "meta3SVideoViews7DClick"},
                    {"id": "meta3SVideoViews7DClick1DView"},
                    {"id": "meta3SVideoViewsDefault"},
                    {"id": "impressions"},
                ]
            }
            response = requests.post("https://api.northbeam.io/v1/exports/data-export", json=payload, headers=headers)
            result = response.json()
            print("result>>>", result)
            export_id = result.get('id')
            print("export_id>>>", export_id)
    
            url = self.get_export_status(export_id)
            print("url>>>", url)
            if url:
                yesterday = datetime.now() - timedelta(1)
                # file_name = f"data_{yesterday.year}_{yesterday.month}_{yesterday.day}.csv"
                file_name = f"data_historical.csv"
        
                response = requests.get(url)

                file_path = f"/tmp/{file_name}"  # Use /tmp for Glue job compatibility
                with open(file_path, 'wb') as f:
                    f.write(response.content)
        
                s3_bucket_name = "shoplc-processed-datalake"
                folder_name = "tjc-northbeam-data"
                self.upload_file_to_s3(s3_bucket_name, folder_name,file_name, file_path)
        
                # Write as parquet file so it can be transferred to Athena as well
                parquet_file_path = "/tmp/data_historical.parquet"  
                with open(parquet_file_path, 'wb') as f:
                    f.write(response.content)
                self.upload_file_to_s3("tjc-processed-data", "processed-files/northeam_data_v2", "northeam_data_v2.parquet", parquet_file_path)
    
                self.transfer_to_mongodb(file_path, self.mongo_connection_url, self.dbname, self.collection_name)
                print("Data transferred to MongoDB successfully")
            else:
                print("No file URL found in the export result.")
        
            message = f"Glue job 'banavo_tjc_northbeam_data_pipeline' was successful!"
            status = 'SUCCESS'
            client="TJC"
            output = self.notify_on_slack(message=message, status=status,client=client)
            print(output)
        except Exception as e:
            message = 'banavo_tjc_northbeam_data_pipeline'
            status = 'FAILURE'
            error = str(e)
            stackTrace = traceback.format_exc()
            client="TJC"
    
            # print(status, message, error, stackTrace)
    
            output = self.notify_on_slack(message=message, status=status, error=error, stackTrace=stackTrace,client=client)
            print(output)
            raise Exception(f"banavo_tjc_northbeam_data_pipeline - job failed. {e}")
        
    def str_to_bool(self, value):
        if isinstance(value, bool):
            return value

        value = value.strip().lower()
        if value in {"true", "1", "yes", "y"}:
            return True
        elif value in {"false", "0", "no", "n"}:
            return False
        else:
            raise ValueError(f"Cannot convert string '{value}' to a boolean.")
        
    def parse_s3_path(self, s3_path):
        parsed = urlparse(s3_path)
        bucket = parsed.netloc
        prefix = parsed.path.strip("/")
        return bucket, prefix
    
    def read_json_from_s3(self, json_path):
        """Reads a JSON configuration file from S3."""
        print(f"Reading file from: {json_path}")
        bucket, key = self.parse_s3_path(json_path)
        obj = self.s3_client.get_object(Bucket=bucket, Key=key)
        return json.loads(obj["Body"].read().decode("utf-8"))
    
    def get_env_config(self, tjc_configuration, use_production):
        """Retrieve the environment-specific configuration."""
        env = "production" if use_production else "development"
        return tjc_configuration.get("env", {}).get(env, {})

    def get_timezone_from_config(self, s3_path):
        configuration = self.read_json_from_s3(s3_path)
        timezone = configuration.get("timezone", "UTC") 
    
        if timezone == "BST":
            timezone = "Europe/London" # accepted by pytz
        print('returning timezone', timezone)
        return timezone
    
    def convert_to_gmt(self, time):
        gmt = pytz.timezone("GMT")
        return time.astimezone(gmt)
    
    def convert_to_bst(self, time):
        gmt = pytz.timezone("Europe/London")
        return time.astimezone(gmt)
    

    def update_data_load_history(self):
        client = None
        try:
            tjc_configuration = self.read_json_from_s3(self.tjc_configuration_s3_path)
            USE_PRODUCTION = self.use_production

            JOB_NAME = self.job_name
            print(f"USE_PRODUCTION: {USE_PRODUCTION}")

            env_configs = self.get_env_config(tjc_configuration, USE_PRODUCTION)
            mongo_connection_url = env_configs.get("mongodb", {}).get("connection_url", "")
            mongo_database_name = env_configs.get("mongodb", {}).get("db", "")
            transformation_path = tjc_configuration.get("transformations", "")

            client = MongoClient(mongo_connection_url)
            db = client[mongo_database_name]

            if not (mongo_connection_url or mongo_database_name):
                raise ValueError(f"Mongodb credential(s) are missing. Stopping job: {JOB_NAME}")

            northbeam_collection = db["northbeam_data_v2"]
            dataloadhistory_collection = db["dataloadhistory"]
            datarangehistory_collection = db["datarangehistory"]

            # we have transformations path where the timezone and currency are defined
            # (Better if we define in the main configuration file)
            timezone = self.get_timezone_from_config(transformation_path)
            print(f"timezone found: {timezone}")

            try:
                tz = pytz.timezone(timezone)
            except pytz.UnknownTimeZoneError:
                print(f"Unknown timezone '{timezone}', defaulting to UTC.")
                tz = pytz.timezone("UTC")  # pytz doesn't recognize BST timezone

            # Get today's date in the specified timezone
            today_tz = datetime.now(tz)
            today_tz = self.convert_to_gmt(today_tz)
            # today_tz = today_tz.replace(hour=0, minute=0, second=0, microsecond=0)

            # Find and update the earliest and latest Northbeam data timestamps
            earliest_doc = northbeam_collection.find_one(
                {
                    "date": {"$exists": True}
                },  # Only consider documents where the 'date' field exists
                sort=[("date", 1)],
            )
            latest_doc = northbeam_collection.find_one(
                filter={"date": {"$lt": today_tz}}, sort=[("date", -1)]
            )
            if earliest_doc and latest_doc:
                earliest_date = earliest_doc["date"]
                latest_date = latest_doc["date"]

                now_utc = datetime.now(pytz.utc)  # Current UTC time

                bst_earliest_date = self.convert_to_bst(earliest_date)
                bst_latest_date = self.convert_to_bst(latest_date)

                doc = {
                    "updated_at": bst_latest_date,
                    "source": "Northbeam",
                    "meta": {
                        "from_date": bst_earliest_date,
                        "to_date": bst_latest_date,
                        "run_on": now_utc,
                    },
             }
                print("Inserted doc: ", doc)

                dataloadhistory_collection.update_one(
                    {"source": "Northbeam"}, {"$set": doc}, upsert=True
                )

                existing_doc = datarangehistory_collection.find_one(
                    filter={"updated_at": {"$lte": today_tz}, "source": {"$eq": "Northbeam"}},
                    sort=[("updated_at", -1)],
                )
                if existing_doc is None:
                    datarangehistory_collection.insert_one(doc)
                elif existing_doc["updated_at"] == latest_date:
                    print("Skipping duplicate entry")
                else:
                    datarangehistory_collection.insert_one(doc)

            output = self.notify_on_slack(
                status="SUCCESS",
                message=f"Glue job '{JOB_NAME}' completed successfully!",
                client=self.slack_client,
            )

            print(output)

        except Exception as e:
            error_message = str(e)
            stack_trace = traceback.format_exc()
            output = self.notify_on_slack(
                status="FAILURE",
                message=f"Glue job '{JOB_NAME}' failed.",
                error=error_message,
                stackTrace=stack_trace,
                client=self.slack_client,
            )
            print(output)
            print(f"ETL job failed with error: {error_message}")
            raise e

        finally:
            if client:
                client.close()
