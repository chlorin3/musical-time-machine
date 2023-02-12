import re
import requests
from bs4 import BeautifulSoup
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from pprint import pprint

# Prompt user for input until it's correct
while True:
    user_input = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ").strip()

    # Check if input is in correct format
    match = re.fullmatch("\d\d\d\d-\d\d-\d\d", user_input)
    if match:
        break
    else:
        print("Incorrect format. Try again.\n")

# Obtain year from provided date
year = user_input.split("-")[0]

# Get Billboard website with desired chart
response = requests.get(f"https://www.billboard.com/charts/hot-100/{user_input}")
billboard_web_page = response.text

soup = BeautifulSoup(billboard_web_page, "html.parser")

# Create a list with song titles scraped from the Billboard website
chart_list = [{"title": tag.text.strip(), "artist": tag.find_next_sibling().text.strip()} for tag in soup.select(selector=".o-chart-results-list__item > h3")]

if not chart_list:
    sys.exit("This chart does not exist.")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=os.environ.get("SPOTIPY_CLIENT_ID"),
        client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET"),
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

# Search for each song's URI and add it to the list
songs_uris = []
for song in chart_list:
    # NOTE: When artist is in the query, only 70-80% of the songs are found
    # AND more accurate results are with year as range

    result = sp.search(q=f"track:{song['title']} artist:{song['artist']} year:{int(year)-2}-{year}", type="track")

    if not result["tracks"]["items"]:
        result = sp.search(q=f"track:{song['title']} year:{year}", type="track")

    # if not result["tracks"]["items"]:
    #     result = sp.search(q=f"track:{song['title']} year:{int(year) - 1}-{year}", type="track")

    try:
        songs_uris.append(result["tracks"]["items"][0]["uri"].split(":")[-1])
    except IndexError:
        print(f"{song['title']} by {song['artist']} does not exist in Spotify. Skipped.")

# Create a new private playlist
playlist_id = sp.user_playlist_create(user_id, f"{user_input} Billboard 100", public=False, collaborative=False, description='')["id"]

# Add songs to the new playlist
sp.playlist_add_items(playlist_id, songs_uris)
