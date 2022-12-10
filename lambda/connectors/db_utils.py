# encoding: utf-8
import urllib.parse
from typing import Union

from configurations import skill_config
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

client: Union[MongoClient, None] = None


def connect() -> MongoClient:
    global client

    if client is not None:
        try:
            client.server_info()
            return client
        except ServerSelectionTimeoutError:
            pass

    username = urllib.parse.quote_plus(skill_config.DB_USER)
    password = urllib.parse.quote_plus(skill_config.DB_PASS)
    db_url = urllib.parse.quote_plus(skill_config.DB_URL)
    db_name = urllib.parse.quote_plus(skill_config.DB_NAME)

    client = MongoClient(
        f"mongodb+srv://{username}:{password}@{db_url}/{db_name}?retryWrites=true&w=majority&serverSelectionTimeoutMS=3000"
    )

    return client


def close():
    global client

    if client is not None:
        client.close()
        client = None
