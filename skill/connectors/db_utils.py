# encoding: utf-8
from sys import path
import os
from os.path import dirname as dir

path.append(dir(path[0]))

from pymongo import MongoClient
from configurations import skill_config
import urllib

def connect():
    username = urllib.parse.quote_plus(skill_config.DB_USER)
    password = urllib.parse.quote_plus(skill_config.DB_PASS)
    db_url = urllib.parse.quote_plus(skill_config.DB_URL)
    db_name = urllib.parse.quote_plus(skill_config.DB_NAME)
    
    client = MongoClient(f'mongodb+srv://{username}:{password}@{db_url}/{db_name}?retryWrites=true&w=majority')

    return client

def close(client):
    client.close()