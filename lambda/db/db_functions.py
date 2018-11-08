# encoding: utf-8
from sys import path
import os
from os.path import dirname as dir

path.append(dir(path[0]))

from pymongo import MongoClient
import db_utils
from configurations import skill_config

def retrieve_random_question(handler_input):
    req_envelope = handler_input.request_envelope

    user_id = req_envelope.context.System.user.userId

    random_question = __get_question_for_user(user_id)['question']

    return random_question

def __get_question_for_user(user_id):
    question = None

    if not __user_exists(user_id):
        __insert_new_user(user_id)
    
    if __get_number_questions() == __get_number_already_fetched_questions(user_id):
        __reset_user_fetched_questions(user_id)
        
    fetched_questions = __get_already_fetched_questions(user_id)

    question = __get_random_question_not_fetched(fetched_questions)
    
    __add_user_fetched_question(user_id, question['_id'])

    return question

def __add_user_fetched_question(user_id, question_id):
    client = db_utils.connect()
    db = client[skill_config.DB_NAME]

    db.users.find_one_and_update({
        'user_id': user_id
    }, {
        '$push': {
            'fetched_questions': question_id
        }
    })

    db_utils.close(client)


def __get_random_question_not_fetched(already_fetched):
    client = db_utils.connect()
    db = client[skill_config.DB_NAME]

    questions = db.questions.aggregate([
        {
            '$match': {
                '_id': {
                    '$nin': already_fetched
                }
            }
        },
        {
            '$sample': { 'size': 1 }
        }
    ])

    db_utils.close(client)

    return list(questions)[0]

def __reset_user_fetched_questions(user_id):
    client = db_utils.connect()
    db = client[skill_config.DB_NAME]

    db.users.find_one_and_update({
        'user_id': user_id
    }, {
        '$set': {
            'fetched_questions': []
        }
    })

    db_utils.close(client)

def __get_number_questions():
    client = db_utils.connect()
    db = client[skill_config.DB_NAME]

    res = db.questions.count_documents({})

    db_utils.close(client)

    return res

def __get_number_already_fetched_questions(user_id):
    return len(__get_already_fetched_questions(user_id))

def __get_already_fetched_questions(user_id):
    client = db_utils.connect()
    db = client[skill_config.DB_NAME]

    res = db.users.find_one({
        'user_id': user_id
    })

    db_utils.close(client)

    return res['fetched_questions']

def __user_exists(user_id):
    client = db_utils.connect()
    db = client[skill_config.DB_NAME]

    res = db.users.count_documents({
        'user_id': user_id
    })

    db_utils.close(client)

    return res == 1

def __insert_new_user(user_id):
    client = db_utils.connect()
    db = client[skill_config.DB_NAME]

    db.users.insert_one({
        'user_id': user_id,
        'fetched_questions': []
    })