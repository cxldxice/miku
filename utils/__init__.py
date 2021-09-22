import json
from time import time

import spotipy
import youtube_dl
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_search import YoutubeSearch
import json

def get_config():
    return json.load(open("config.json"))

def get_spotify():
    config = get_config()

    return spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            config["spotify"]["client_id"],
            config["spotify"]["client_secret"]
        )
    )

def search_query(query):
    results = YoutubeSearch(query, max_results=1).to_dict()
    return "https://www.youtube.com/watch?v=" + results[0]["id"]

def get_youtube_info(url, query=False):
    out = {}

    if query:
        url = search_query(url)
    
    print(1)
    with youtube_dl.YoutubeDL({'format': 'bestaudio'}) as ydl:
        info = ydl.extract_info(url, download=False)
        out["source"] = info['formats'][0]['url']
        out["title"] = info["title"]
        out["date"] = time() - int(info["upload_date"])
        out["duration"] = info["duration"]
        out["thumbnail"] = info["thumbnail"]

    return out

def has_any_in_string(string, any_strings):
    for any_string in any_strings:
        if any_string in string:
            return True

    return False

def define_input(_input):
    out = {}
    if has_any_in_string(_input, ["http", ".com"]):
        if "playlist" in _input:
            out["playlist"] = True
        else:
            out["playlist"] = False
        
        if "spotify.com" in _input:
            out["service"] = "spotify"
        elif "youtube.com" in _input:
            out["service"] = "youtube"

        out["url"] = True
    else:
        out["url"] = False
        out["query"] = True
        
    return out
