from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

CLIENT_ID = "Enter Yours"
CLIENT_SECRET = "Enter Yours"
REDIRECT_URI = "http://example.com"
DISPLAY_NAME = "Enter Yours"
SCOPE = 'playlist-modify-private playlist-read-private'

travel_to_date = input("Which year would you like to travel back to? YYYY-MM-DD: ")
URL = "https://www.billboard.com/charts/hot-100/" + travel_to_date + "/"

response = requests.get(URL)
page = response.text

soup = BeautifulSoup(page, "html.parser")

song_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_spans]
print(song_names)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        show_dialog=True,
        cache_path="token.txt",
        username=DISPLAY_NAME,
    )
)

user_id = sp.current_user()["id"]

song_URIs = []
year = travel_to_date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_URIs.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{travel_to_date} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_URIs)
