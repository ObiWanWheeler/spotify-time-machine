from bs4 import BeautifulSoup
import requests
import os
import spotipy

BILLBOARD_BASE_URL = "https://www.billboard.com/charts/hot-100/"

date = input("Enter the date you would like to travel to in the YYYY-MM-dd format : ")

response = requests.get(BILLBOARD_BASE_URL + date)
top_100_site = response.text
soup = BeautifulSoup(top_100_site, "html.parser")

top_100_names = [t.getText() for t in soup.select(selector="span .chart-element__information__song")]
print("\n".join(top_100_names))

CLIENT_ID = os.environ["spotify_client_id"]
CLIENT_SECRET = os.environ["spotify_client_secret"]

spotify = spotipy.Spotify(oauth_manager=spotipy.
                          SpotifyOAuth(client_id=CLIENT_ID,
                                       client_secret=CLIENT_SECRET,
                                       redirect_uri="http://example.com",
                                       scope="playlist-modify-private"))
user_id = spotify.current_user()["id"]

song_uris = []
for song in top_100_names:
    track_data = spotify.search(q=f"track: {song} year:{date[0:4]}", limit=1)["tracks"]["items"]
    if len(track_data) != 0:
        uri = track_data[0]["uri"]
        song_uris.append(uri)
    else:
        print(f"{song} does not exist in Spotify.")

playlist_id = spotify.user_playlist_create(user=user_id,
                                           name=f"{date} Billboard Top 100",
                                           public=False,
                                           description=f"The top 100 songs on {date}")["id"]
print(playlist_id)

spotify.playlist_add_items(playlist_id, song_uris)
