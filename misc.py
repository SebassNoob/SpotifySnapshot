
import requests
import json
import datetime
import sqlite3

import aiohttp
import asyncio

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
  #returns both the url and the id of the playlist
  return (f'https://open.spotify.com/playlist/{new_playlist_id}', new_playlist_id)
    




def get_playlist_info(auth:str, id:int):
  
  '''grabs playlist information given id'''
  

  #constant headers for all required requests
  headers_const = {
    "Content-Type":"application/json",
    "Authorization": f"Bearer {auth.get('access_token')}",
    "Host": "api.spotify.com"
  }

  request_urls = [
    f'https://api.spotify.com/v1/playlists/{id}/tracks',
    f'https://api.spotify.com/v1/playlists/{id}'
  ]
  async def request(list_urls:list):
    async with aiohttp.ClientSession(headers=headers_const) as session:
      responses = []
      for url in request_urls:
        async with session.get(url) as resp:
          responses.append(await resp.json())
          
    return responses

  
  res= asyncio.run(request(request_urls))
  
  
  return res




def get_user_data(auth:str):
  headers_const = {
    "Content-Type":"application/json",
    "Authorization": f"Bearer {auth.get('access_token')}",
    "Host": "api.spotify.com"
  }
  user = requests.get('https://api.spotify.com/v1/me', headers = headers_const )
    
    
  return Credentials(json.loads(user.text).get('id'), json.loads(user.text).get('display_name'), json.loads(user.text).get('images')[0].get("url"))
  
def get_connection(path):
  #returns connection and cursor object
  con = sqlite3.connect(path)
  cur= con.cursor()
  return (con,cur)


def synchronize_async_helper(to_await):
  '''runs async funcs synchronously'''
  async_response = []

  async def run_and_capture_result():
    r = await to_await
    async_response.append(r)
  
  loop = asyncio.get_event_loop()
  coroutine = run_and_capture_result()
  loop.run_until_complete(coroutine)
  return async_response[0]