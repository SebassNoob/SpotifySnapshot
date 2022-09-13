import os
from flask import Flask, redirect, request, make_response, render_template, flash

import datetime
import sqlite3
from pathlib import Path
import string
import random
import requests
import base64
import json 
import logging

from misc import make_playlist, get_user_data, get_connection
from db.init_db import create_db

log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)




id = os.environ['id']
secret = os.environ['secret']
scope = "user-library-read user-top-read playlist-modify-public"





  


app = Flask(__name__)

def debug_sql(id):
  con = sqlite3.connect(id).cursor()
  data = con.execute("SELECT * FROM endUser").fetchall()
  for row in data:
    print(row)




@app.route('/')
def index():
  
  return render_template('index.html')

@app.route('/temp')
def temp():
  return render_template('getit.html')


@app.route('/getit', methods = ['GET','POST'])
def getit():
  if request.method == 'GET':
    if request.cookies.get('auth') is not None:
      
      return render_template('getit.html')
    else: 
      return render_template('getit-error.html'), {"Refresh": "7; url=/"}

  
  if request.method == 'POST':

    #TODO: get all the params and redirect to /history/id
    #TODO: add a "history" <a> tag in index.html
    
    auth = json.loads(base64.b64decode(request.cookies.get('auth')))
    creds= get_user_data(auth)
    #creates a user profile if not exists
    if not Path(f'./db/data/{creds.id}.db').is_file():
      
      create_db(creds.id)
      
    
    try:
      url = make_playlist(auth, request.form['name'], request.form['length'])

      conn, cur = get_connection(f'./db/data/{creds.id}.db')
      
      cur.execute('INSERT INTO endUser (created, url) VALUES (?,?)', (f"{datetime.datetime.today().strftime('%d-%m-%Y')}", url))
      conn.commit()
      conn.close()
      debug_sql(f'./db/data/{creds.id}.db')
      
    
      
    except Exception as e:
      print(e)
      return redirect('/error/500', 302)
    return 'hello world'
  #if accessed without logging/cookies, return to homepage and force to login
  return render_template('getit-error.html'), {"Refresh": "7; url=/"}

@app.route('/history')
def history():
  '''history homepage'''
  return 'hi'

@app.route('/history/<id>')
def history_pages(id):
  '''a list of past playlists'''
  return id



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