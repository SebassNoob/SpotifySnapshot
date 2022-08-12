import os
from flask import Flask, redirect, request, make_response, render_template, flash

from dataclasses import dataclass
import string
import random
import requests
import base64
import json 
import logging
import datetime


log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)



@dataclass
class Credentials:
  id: str
  secret: str
  scope: str


id = os.environ['id']
secret = os.environ['secret']
scope = "user-library-read user-top-read playlist-modify-public"

months_of_the_year = ['January', 'February', 'March','April','May','June','July','August','September','October','November','December']



app = Flask(__name__)



@app.route('/')
def index():
  
  return render_template('index.html')

@app.route('/temp')
def temp():
  return render_template('getit.html')

@app.route('/getit')
def getit():
  if request.cookies.get('auth') is not None:
    '''if user has cookie with encoded auth token, take that to process'''
    
    auth = json.loads(base64.b64decode(request.cookies.get('auth')))

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
    
    return str(json.loads(new_playlist.text).get('external_urls').get('spotify'))
  #if accessed without logging/cookies, return to homepage and force to login
  return render_template('getit-error.html'), {"Refresh": "7; url=/"}


@app.route('/login')
def login():
  state = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
  
  return redirect('https://accounts.spotify.com/authorize?'+f'response_type=code&client_id={id}&scope={scope}&redirect_uri=https://spotifysnapshot.sebassnoob.repl.co/callback&state={state}&show_dialog=true')
  

@app.route('/callback')
def callback():
  '''handles callbacks from authentication requests'''

  
  res = request.args.to_dict()
  if 'error' in res.keys():
    #if the thing errors out, do this. 
    #TODO:render an error page
    return redirect('/error/403', 302)
  elif 'code' in res.keys():
    #received auth code! now to obtain the access token
    #send a post request to https://accounts.spotify.com/api/token endpoint

    #this sets the authorisation header
    #encodes this string in base64 bytes, then converts back to string
    auth_id_secret = base64.b64encode((f'{id}:{secret}').encode('ascii')).decode('utf-8')
    
    
    r = requests.post('https://accounts.spotify.com/api/token', headers ={
      'Authorization': f'Basic {auth_id_secret}',
      'Content-Type':'application/x-www-form-urlencoded'
      
    },
    data={
      'grant_type':'authorization_code',
      'code' : res['code'],
      'redirect_uri':'https://spotifysnapshot.sebassnoob.repl.co/callback',
      'client_id':id,
      'code_verifier':res['state']
    })
    
    if 'error' not in r.json().keys():

      resp = make_response(redirect('/', 302))
      resp.set_cookie('auth',base64.b64encode(r.text.encode('ascii')), max_age=r.json().get('expires_in'))
      
      return resp
    return redirect('/error/400', 302)


@app.route('/error/<id>')
def error(id):
  return id

  
app.run(host='0.0.0.0', port = 8080, debug=True)