import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

#we created seperated .env file to get api key
API_KEY=os.getenv("API_KEY")
Channel_handle="MrBeast"

def get_playlist_id():
    try:
       url=f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={Channel_handle}&key={API_KEY}"

       response=requests.get(url)


       #print(response)
       data=response.json()

       #json.dumps convert python object in to json formatted string ..
       #we use indent form as it is common convention in python for code readability.
       #print(json.dumps(data,indent=4))

       channel_items=data['items'][0]
       channel_playlistid=channel_items['contentDetails']['relatedPlaylists']['uploads']

       print(channel_playlistid)
       return channel_playlistid

    except requests.exceptions.RequestException as e:
        raise e   

if __name__ == "__main__":
    get_playlist_id()    