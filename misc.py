
import requests
import json
import datetime

from dataclasses import dataclass
@dataclass
class Credentials:
  '''access to essential information of user'''
  id: str
  display_name: str
  avatar: str

def make_playlist(auth:str, name: str, length: int):
  
  months_of_the_year = ['January', 'February', 'March','April','May','June','July','August','September','October','November','December']
  

  #constant headers for all required requests
  headers_const = {
    "Content-Type":"application/json",
    "Authorization": f"Bearer {auth.get('access_token')}",
    "Host": "api.spotify.com"
  }
  user = requests.get('https://api.spotify.com/v1/me', headers = headers_const )
    #yoink the username and id for playlist creation
    
  username = json.loads(user.text).get('display_name')
  userid = json.loads(user.text).get('id')
    
    #get users top songs
  songs = requests.get('https://api.spotify.com/v1/me/top/tracks', headers = headers_const, params = {
    'limit':30,
    'offset':0,
    'time_range':'short_term'
  })
    
  uris = []
  for song in json.loads(songs.text).get('items'):
    uris.append(song.get('uri'))


    #creates a new playlist
  new_playlist = requests.post(f'https://api.spotify.com/v1/users/{userid}/playlists', headers = headers_const, data=json.dumps({
    'name': f"{username}'s favourite songs of {months_of_the_year[datetime.datetime.today().month-1]} {datetime.datetime.today().year}",
    'description':f"top songs of {username} as of {datetime.datetime.today()}"
  }))

    #grabs the id to append to 
  new_playlist_id = json.loads(new_playlist.text).get('id')

  requests.post(f'https://api.spotify.com/v1/playlists/{new_playlist_id}/tracks', headers = headers_const, data = json.dumps({

    'uris':uris,
    'position':0
        
      
  }))
  return
    




def get_user_data(auth:str):
  headers_const = {
    "Content-Type":"application/json",
    "Authorization": f"Bearer {auth.get('access_token')}",
    "Host": "api.spotify.com"
  }
  user = requests.get('https://api.spotify.com/v1/me', headers = headers_const )
    #yoink the username and id for playlist creation
    
  return Credentials(json.loads(user.text).get('id'), json.loads(user.text).get('display_name'), json.loads(user.text).get('images')[0].get("url"))
  
  