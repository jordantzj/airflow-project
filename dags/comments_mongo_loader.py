import os
import json
from pymongo import MongoClient

from dotenv import load_dotenv
load_dotenv()
IP_ADDRESS = os.getenv("IP_ADDRESS")

# Load function: Reads data from a JSON file and inserts it into MongoDB
def load_comments_to_mongo(json_file, mongo_uri, db_name, collection_name):
    # Create a MongoDB client
    try:
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]

        # Read the JSON data from the file
        with open(json_file, 'r') as file:
            data = [json.loads(line) for line in file]  # Read each line and convert to dictionary

        # Insert data into MongoDB
        result = collection.insert_many(data)
        print(f"Successfully inserted {len(result.inserted_ids)} comments into MongoDB collection '{collection_name}'.")

    except Exception as e:
        print(f"An error occurred while inserting data into MongoDB: {e}")
    finally:
        # Close the MongoDB connection
        client.close()

    # Delete the JSON file after the data has been inserted
    try:
        os.remove(json_file)
        print(f"Deleted file {json_file} after inserting into MongoDB.")
    except Exception as e:
        print(f"An error occurred while deleting the file: {e}")

# Main function
if __name__ == "__main__":
    # MongoDB connection details
    MONGO_URI = f"mongodb://{IP_ADDRESS}:27017/" # Get IP Address from .env file
    DB_NAME = "youtube_data"  # Replace with your desired database name
    COLLECTION_NAME = "youtube_comments"  # Collection to store comments

    # Path to the JSON file
    JSON_FILE = "youtube_comments.json"

    # Load the comments into MongoDB and delete the JSON file
    load_comments_to_mongo(JSON_FILE, MONGO_URI, DB_NAME, COLLECTION_NAME)
