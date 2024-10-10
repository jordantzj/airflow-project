import os
import pandas as pd
from googleapiclient.discovery import build
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

# Extract function: Retrieves comments from a YouTube video using YouTube API
def extract_comments(video_id, api_key):
    # Build a service object for YouTube Data API v3
    youtube = build('youtube', 'v3', developerKey=api_key)

    comments = []
    try:
        # Call the API to fetch comments for the video
        request = youtube.commentThreads().list(
            part='snippet,replies',
            videoId=video_id,
            maxResults=100
        )

        while request:
            response = request.execute()
            # Loop through comments and append to list
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                user_id = item['snippet']['topLevelComment'].get('authorChannelId', {}).get('value', 'Unknown')  # Safely extract user_id
                comments.append({
                    'user_id': user_id,  # Use safely extracted user ID
                    'author': comment['authorDisplayName'],
                    'comment': comment['textOriginal'],
                    'published_at': comment['publishedAt'],
                    'like_count': comment['likeCount']
                })
            # Check if there's a next page
            request = youtube.commentThreads().list_next(request, response)

    except Exception as e:
        print(f"An error occurred: {e}")

    return comments

# Transform function: Cleans and structures the extracted comments
def transform_comments(comments):
    # Convert list of dictionaries to DataFrame for easy transformation
    df = pd.DataFrame(comments)

    # Optional transformations (e.g., removing emojis, handling missing values)
    df['comment'] = df['comment'].str.replace(r'[^\x00-\x7F]+', '', regex=True)  # Remove non-ASCII characters
    df['published_at'] = pd.to_datetime(df['published_at'])  # Convert to datetime
    df = df.drop_duplicates()  # Remove duplicate comments

    return df

# Load function: Saves the transformed data to a JSON file
def load_comments_to_json(df, output_file):
    try:
        # Save DataFrame to JSON
        df.to_json(output_file, orient='records', lines=True)
        print(f"Comments successfully saved to {output_file}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")

# ETL pipeline function to combine the process
def youtube_comments_etl(video_id, api_key, output_file):
    # Step 1: Extract
    comments = extract_comments(video_id, api_key)

    if comments:
        # Step 2: Transform
        transformed_comments = transform_comments(comments)

        # Step 3: Load
        load_comments_to_json(transformed_comments, output_file)
    else:
        print("No comments were retrieved.")

# Main function
if __name__ == "__main__":
    # Define YouTube API key and video ID
    API_KEY = API_KEY
    VIDEO_ID = "tQcnTfu6Izs"
    OUTPUT_FILE = "youtube_comments.json"

    # Run the ETL process
    youtube_comments_etl(VIDEO_ID, API_KEY, OUTPUT_FILE)
