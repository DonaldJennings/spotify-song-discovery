import pandas as pd
import spotipy
import json

trackNo = 0
def get_artists_from_song(track):
    return ','.join([artist['name'] for artist in track['artists']])

def get_user_songs(client: spotipy.Spotify):
    results = client.current_user_saved_tracks()
    tracks = results['items']
    while results['next']:
        results = client.next(results)
        tracks.extend(results['items'])
    return tracks

def get_features(client: spotipy.Spotify, track):
    print("Processing " + track['name'])
    features = client.audio_features(track['id'])
    return features[0]
    
def process_songs(client, tracks):
    """Returns a Pandas Dataframe of all the tracks

    Args:
        tracks (dict): Dictionary of tracks, expected input from client.current_user_saved_tracks()
    """
    trackList = []
    for index, item in enumerate(tracks):
        track = item['track']
        features = get_features(client, track)
        trackObj = {
            "track_name" : track['name'],
            "artists" : get_artists_from_song(track),
            "danceability" : features['danceability'],
            "key" : features['key'],
            "energy" : features['energy'],
            "loudness" : features['loudness'],
            "speechiness" : features['speechiness'],
            "acousticness" : features['acousticness'],
            "instrumentalness" : features['instrumentalness'],
            "liveness" : features['liveness'],
            "valence" : features['valence'],
            "tempo" : features['tempo'],
            "duration_ms" : features['duration_ms'],
            "time_signature" : features['time_signature'],
            "track_id" : track['id'], 
        }
        trackList.append(trackObj)
    trackNo = 0
    return pd.DataFrame.from_dict(trackList, orient='columns')
        