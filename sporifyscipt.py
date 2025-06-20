import requests
import pandas as pd

# ✅ Function to get Spotify access token
def get_spotify_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, data={
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    auth_data = auth_response.json()
    return auth_data['access_token']

# ✅ Function to search for a track and get its ID
def search_track(track_name, artist_name, token):
    query = f"{track_name} artist:{artist_name}"
    url = f"https://api.spotify.com/v1/search?q={requests.utils.quote(query)}&type=track&limit=1"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    json_data = response.json()
    try:
        track_id = json_data['tracks']['items'][0]['id']
        return track_id
    except (KeyError, IndexError):
        return None

# ✅ Function to get track details (e.g., image URL)
def get_track_details(track_id, token):
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    json_data = response.json()
    try:
        image_url = json_data['album']['images'][0]['url']
        return image_url
    except (KeyError, IndexError):
        return None

# 🔐 Your Spotify API credentials
client_id = '6556d3ca786244659b4537d1ae7ccb49'
client_secret = 'd637bb013a044b96bf38fe521e65a848'

# 🎟️ Get Access Token
access_token = get_spotify_token(client_id, client_secret)

# 📄 Read your CSV and clean column names
df_spotify = pd.read_csv('spotify-2023.csv', encoding='ISO-8859-1')
df_spotify.columns = df_spotify.columns.str.strip().str.lower()
print("CSV Columns:", df_spotify.columns.tolist())  # Debug line

# 🔁 Loop and get images
df_spotify['image_url'] = None
for i, row in df_spotify.iterrows():
    track_id = search_track(row['track_name'], row['artist(s)_name'], access_token)
    if track_id:
        image_url = get_track_details(track_id, access_token)
        df_spotify.at[i, 'image_url'] = image_url

# 💾 Save updated file
df_spotify.to_csv('updated_file.csv', index=False)
print("✅ CSV updated with image URLs.")
