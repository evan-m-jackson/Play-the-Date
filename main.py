from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth



date = input("Which day do you want to travel to? Type the date in this format YYYY-MM-DD: ")

URL = f"https://www.billboard.com/charts/hot-100/{date}"
CLIENT_ID = INSERT CLIENT ID FROM SPOTIFY WEBSITE
CLIENT_SECRET = INSERT CLIENT SECRET FROM SPOTIFY WEBSITE
REDIRECT_URI = 'https://example.com'

response = requests.get(URL)
billboard_webpage = response.text

soup = BeautifulSoup(billboard_webpage, "html.parser")
song_list = soup.find_all(name='span', class_="chart-element__information__song text--truncate color--primary")
billboard_100 = []

for song in song_list:
    billboard_100.append(song.getText())

scope = "playlist-modify-private"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope,
                              show_dialog=True, cache_path="token.txt"))

results = sp.current_user()
user_id = results['id']

spotify_uri_list = []

for song in billboard_100:
    result = sp.search(q=f"track: {song} year:{date[:4]}")

    try:
        spotify_uri_list.append(result['tracks']['items'][0]['uri'])
    except IndexError:
        pass

playlist = sp.user_playlist_create(user_id, f"{date} Billboard 100", public=False, )
playlist_id = playlist['id']

sp.playlist_add_items(playlist_id, spotify_uri_list)
