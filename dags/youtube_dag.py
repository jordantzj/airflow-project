from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from datetime import datetime
from random import randint
from airflow.operators.bash import BashOperator

import sys
import os
from dotenv import load_dotenv

from comments_collector import youtube_comments_etl
from comments_mongo_loader import load_comments_to_mongo
load_dotenv()
API_KEY = os.getenv("API_KEY")
IP_ADDRESS = os.getenv("IP_ADDRESS")

# Wrapper function to pass arguments to youtube_comments_etl
def run_youtube_etl():
    youtube_comments_etl("m6SOJlkN1zU", API_KEY, "youtube_comments.json")

def run_mongo_loader():
    load_comments_to_mongo("youtube_comments.json", f"mongodb://{IP_ADDRESS}:27017/", "youtube_data", "youtube_comments")

with DAG("youtube_dag", start_date=datetime(2024,1,1),
    schedule_interval = "@daily", catchup=False) as dag:
        commentsCollector = PythonOperator(
            task_id ="comments_collector",
            python_callable = run_youtube_etl
)

        commentsMongoLoader = PythonOperator(
            task_id ="comments_mongo_loader",
            python_callable = run_mongo_loader
)


commentsCollector >> commentsMongoLoader
