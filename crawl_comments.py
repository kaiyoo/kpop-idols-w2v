import googleapiclient.discovery
import pandas as pd
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from googleapiclient.errors import HttpError
import time
import tqdm

DetectorFactory.seed = 0

# YouTube API key
API_KEY = "YOUR-API-KEY"

youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)
VIDEO_PER_ARTIST_MAX_LIMIT = 50
COMMENTS_PER_VIDEO_MAX_LIMIT= 50

# artist*video*comments: 100*50*100
# Get video from query (idol group title)
def get_video_ids(query, max_results=50):
    video_ids = []
    try:
        request = youtube.search().list(
            q=query,
            part="snippet",
            maxResults=max_results,
            type="video"
        )
        response = request.execute()
            
        # Only check if 'id' key exists and 'videoId' is accessible
        for item in response['items']:
            if isinstance(item, dict) and 'id' in item and 'videoId' in item['id']:
                video_ids.append(item['id']['videoId'])
                
    except HttpError as e:
        error_reason = e.resp.get('reason')
        if error_reason == 'quotaExceeded':
            print("Quota exceeded. Saving collected data...")
            save_data_to_csv(video_comments)
            exit()
        else:
            print(f"An error occurred: {e}")
    return video_ids

# Get comments for 1 video
def get_top_korean_comments(video_id, max_results=100, top_k=COMMENTS_PER_VIDEO_MAX_LIMIT):

    comments = []
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results,
            textFormat="plainText"
        )
        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            try:
                # Add only Korean comments after language detection
                if detect(comment) == 'ko':
                    comments.append(comment)
                if len(comments) >= top_k:
                    break
            except LangDetectException:
                continue
            
    except HttpError as e:
        error_reason = e.resp.get('reason')
        if error_reason == 'commentsDisabled':
            print(f"Comments are disabled for video {video_id}. Skipping.")
        else:
            print(f"An error occurred: {e}")
    
    return comments


# Make data to dataframe
def save_data_to_csv(video_comments):    
    data = {"Video_ID": [], "Artist": [], "Comment": []}
    for artist, video_data in video_comments.items():
        for video_id, comments in video_data.items():
            for comment in comments:
                data["Video_ID"].append(video_id)
                data["Artist"].append(artist)
                data["Comment"].append(comment)

    df = pd.DataFrame(data)
    print(f"data size: {len(df)}")
    
    # Export to CSV 
    df.to_csv("youtube_comments.csv", index=False)


file_path = "idol_list.txt"
idol_list = []
# read idols and put them in a list
with open(file_path, "r", encoding="utf-8") as file:
    next(file)  # skip column line
    for line in file:
        columns = line.strip().split("\t")  
        if len(columns) > 1: 
            idol_list.append(columns[1])  


video_comments = {}
for query in tqdm.tqdm(idol_list):
    start = time.time()
    
    try:
        video_ids = get_video_ids(query)
        video_comments[query] = {}  # dictionary for each artist
        for video_id in video_ids:
            comments = get_top_korean_comments(video_id)
            video_comments[query][video_id] = comments  # {artist: {video_id: comments}}
    except HttpError as e:
        if e.resp.get('reason') == 'quotaExceeded':
            print("Quota exceeded. Saving collected data...")
            save_data_to_csv(video_comments)
            exit()
            
    end = time.time()    
    print(f"{end - start}s for {query}")
    
save_data_to_csv(video_comments)
