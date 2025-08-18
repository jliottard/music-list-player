# Import Spotify playlists and liked songs into "output_playlists.txt" and "output_liked_songs.txt" in a "imported_playlist" directory.
# Using the format by line : <artist name> - <song name> (<spotify url>) #<playlist name> #spotify

import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

RELATIVE_OUTPUT_DIRECTORY_PATH = "imported_playlist"

OUTPUT_PLAYLISTS_FILE = "output_playlist.txt"
OUTPUT_LIKED_SONGS_FILE = "output_liked_songs.txt"

def get_spotify_crendentials():
    with open("spotify_credentials.json", "rt", encoding="utf-8") as credentials_file:
        credentials: dict = json.load(credentials_file)
        return credentials

if __name__ == "__main__":
    credentials = get_spotify_crendentials()

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=credentials["SPOTIFY_CLIENT_ID"],
        client_secret=credentials["SPOTIFY_SECRET"],
        redirect_uri=credentials["SPOTIFY_REDIRECT_URI"], # use the URL provided in the spotify_credentials.json file
        scope="user-library-read"
    ))

    # Import the playlists using the spotify_playlists.json
    with open("spotify_playlists.json", "rt", encoding="utf-8") as playlists_file:
        playlists = json.load(playlists_file)
        for playlist in playlists:
            list_name = playlist["SPOTIFY_PLAYLIST_NAME"]
            list_id = playlist["SPOTIFY_PLAYLIST_ID"] # the id being the sequence of number and letters in the URL 'https://open.spotify.com/playlist/'
            formatted_for_tag_list_name = list_name.replace(" ", "_")
            formatted_for_tag_list_name = formatted_for_tag_list_name.lower()
            formatted_for_tag_list_name.strip("_")
            passed_tracks = 0
            response = sp.playlist_tracks(playlist_id=list_id)
            n_tracks = response['total']
            while passed_tracks < n_tracks:
                for idx, item in enumerate(response['items']):
                    track = item['track']
                    track_name = track['name']
                    track_artist = track['artists'][0]['name']
                    if len(track['artists']) > 1:
                        for artist in track['artists'][1:]:
                            track_artist += f" and {artist['name']}"
                    track_url = track['external_urls']['spotify']
                    track_tag = f"#{list_name} #spotify"
                    with open(os.path.join(RELATIVE_OUTPUT_DIRECTORY_PATH, OUTPUT_PLAYLISTS_FILE), "at", encoding="utf-8") as playlists_file:
                        playlists_file.write(f"{track_artist} - {track_name} ({track_url}) {track_tag}\n")
                passed_tracks += len(response['items'])
                response = sp.playlist_tracks(playlist_id=list_id)

    # Import the "liked songs"
    passed_tracks = 0
    response = sp.current_user_saved_tracks()
    n_tracks = response['total']
    while passed_tracks < n_tracks:
        for idx, item in enumerate(response['items']):
            track = item['track']
            track_name = track['name']
            track_artist = track['artists'][0]['name']
            if len(track['artists']) > 1:
                for artist in track['artists'][1:]:
                    track_artist += f" and {artist['name']}"
            track_url = track['external_urls']['spotify']
            track_tag = "#spotify"
            # Do not import songs that are already in a playlist 
            with open(os.path.join(RELATIVE_OUTPUT_DIRECTORY_PATH, OUTPUT_PLAYLISTS_FILE), "rt", encoding="utf-8") as playlists_file:
                contents = playlists_file.read()
                if track_name in contents:
                    continue
            with open(OUTPUT_LIKED_SONGS_FILE, "at", encoding="utf-8") as liked_songs_file:
                liked_songs_file.write(f"{track_artist} - {track_name} ({track_url}) {track_tag}\n")
        passed_tracks += len(response['items'])
        response = sp.current_user_saved_tracks(offset=passed_tracks)
