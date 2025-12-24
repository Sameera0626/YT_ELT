import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

#we created seperated .env file to get api key
API_KEY=os.getenv("API_KEY")
Channel_handle="MrBeast"
max_results=50

def get_playlist_id():
    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={Channel_handle}&key={API_KEY}"

        response = requests.get(url)
        data = response.json()

        channel_items = data['items'][0]
        channel_playlistid = channel_items['contentDetails']['relatedPlaylists']['uploads']

        return channel_playlistid

    except requests.exceptions.RequestException as e:
        raise e


def get_video_ids(playlistid):
    videos_ids = []
    pageToken = None

    base_url = (
        f"https://youtube.googleapis.com/youtube/v3/playlistItems"
        f"?part=contentDetails"
        f"&maxResults={max_results}"
        f"&playlistId={playlistid}"
        f"&key={API_KEY}"
    )

    try:
        while True:
            url = base_url

            if pageToken:
                url += f"&pageToken={pageToken}"

            response = requests.get(url)
            response.raise_for_status()

            data = response.json()

            for item in data.get('items', []):
                video_id = item['contentDetails']['videoId']
                videos_ids.append(video_id)

            pageToken = data.get('nextPageToken')

            if not pageToken:
                break
                  
        return videos_ids
    except requests.exceptions.RequestException as e:
        raise e


def extract_video_data(video_ids):
    extracted_data = []

    # Helper function to split list into batches
    def batch_list(video_id_list, batch_size):
        for video_id in range(0, len(video_id_list), batch_size):
            yield video_id_list[video_id:video_id + batch_size]

    try:
        for batch in batch_list(video_ids, max_results):
            video_ids_str = ",".join(batch)

            url = (
                f"https://youtube.googleapis.com/youtube/v3/videos"
                f"?part=snippet,contentDetails,statistics"
                f"&id={video_ids_str}"
                f"&key={API_KEY}"
            )

            response = requests.get(url)
            response.raise_for_status()

            data = response.json()

            for item in data.get("items", []):
                video_id=item["id"]
                snippet = item["snippet"]
                contentDetails = item["contentDetails"]
                statistics = item["statistics"]

                video_data = {
                    "video_id": video_id,
                    "title": snippet["title"],
                    "publishedAt": snippet["publishedAt"],
                    "duration": contentDetails["duration"],
                    "viewCount": statistics.get("viewCount",None),
                    "likeCount": statistics.get("likeCount",None),
                    "commentCount": statistics.get("commentCount",None)
                }

                extracted_data.append(video_data)

        return extracted_data

    except requests.exceptions.RequestException as e:
        raise e
    


if __name__ == "__main__":
    playlistid = get_playlist_id()
    video_ids=get_video_ids(playlistid)
    print(extract_video_data(video_ids))



