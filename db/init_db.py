import sqlite3
import os 
from pathlib import Path

def create_db(id):
  
  
  if os.path.exists(f"db/data/{id}.db"):
    return False
  open(f"db/data/{id}.db", 'w+')
  connection = sqlite3.connect(f'db/data/{id}.db')
  
  with open('db/schema.sql') as f:
    connection.executescript(f.read())
  
  connection.commit()
  connection.close()
  return True
