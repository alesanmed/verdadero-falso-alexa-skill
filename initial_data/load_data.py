# encoding: utf-8
import json
import urllib.parse

from pymongo import MongoClient

from initial_data.configurations import skill_config


def connect() -> MongoClient:
    username = urllib.parse.quote_plus(skill_config.DB_USER)
    password = urllib.parse.quote_plus(skill_config.DB_PASS)
    db_url = urllib.parse.quote_plus(skill_config.DB_URL)
    db_name = urllib.parse.quote_plus(skill_config.DB_NAME)

    client = MongoClient(
        f"mongodb+srv://{username}:{password}@{db_url}/{db_name}?retryWrites=true&w=majority"
    )

    return client


def close(client: MongoClient):
    client.close()


def load_data():
    client = connect()

    db = client.get_database(skill_config.DB_NAME)

    questions = json.load(open("questions.json", "r", encoding="utf-8"))

    db.questions.insert_many(questions)

    close(client)


if __name__ == "__main__":
    load_data()
