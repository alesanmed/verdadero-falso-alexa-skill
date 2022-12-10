# encoding: utf-8
from typing import Any, Dict, List, Union

from ask_sdk_core.handler_input import HandlerInput
from bson import ObjectId
from configurations import skill_config
from connectors import db_utils


def retrieve_random_question(handler_input: HandlerInput) -> Dict[str, Any]:
    req_envelope = handler_input.request_envelope

    user_id = (
        req_envelope.context
        and req_envelope.context.system
        and req_envelope.context.system.user
        and req_envelope.context.system.user.user_id
    )

    random_question = __get_question_for_user(user_id)

    return random_question


def get_question(question_id: str) -> Dict[str, Any]:
    client = db_utils.connect()
    db = client.get_database(skill_config.DB_NAME)

    question = db.questions.find_one({"_id": ObjectId(question_id)})

    if question is None:
        raise LookupError()

    return question


def __get_question_for_user(user_id: Union[str, None]) -> Dict[str, Any]:
    assert user_id is not None

    question = None

    if not __user_exists(user_id):
        __insert_new_user(user_id)

    if __get_number_of_questions() == __get_number_of_already_fetched_questions(
        user_id
    ):
        __reset_user_fetched_questions(user_id)

    fetched_questions = __get_already_fetched_questions(user_id)

    question = __get_random_question_not_fetched(fetched_questions)

    __add_user_fetched_question(user_id, question["_id"])

    return question


def __add_user_fetched_question(user_id, question_id):
    client = db_utils.connect()
    db = client.get_database(skill_config.DB_NAME)

    db.users.find_one_and_update(
        {"user_id": user_id}, {"$push": {"fetched_questions": question_id}}
    )


def __get_random_question_not_fetched(already_fetched: List[str]) -> Dict[str, Any]:
    client = db_utils.connect()
    db = client.get_database(skill_config.DB_NAME)

    questions = db.questions.aggregate(
        [{"$match": {"_id": {"$nin": already_fetched}}}, {"$sample": {"size": 1}}]
    )

    return list(questions)[0]


def __reset_user_fetched_questions(user_id: str):
    client = db_utils.connect()
    db = client.get_database(skill_config.DB_NAME)

    db.users.find_one_and_update(
        {"user_id": user_id}, {"$set": {"fetched_questions": []}}
    )


def __get_number_of_questions() -> int:
    client = db_utils.connect()
    db = client.get_database(skill_config.DB_NAME)

    res = db.questions.count_documents({})

    return res


def __get_number_of_already_fetched_questions(user_id: str):
    return len(__get_already_fetched_questions(user_id))


def __get_already_fetched_questions(user_id: str) -> List[str]:
    client = db_utils.connect()
    db = client.get_database(skill_config.DB_NAME)

    res = db.users.find_one({"user_id": user_id})

    if res is None:
        raise LookupError()

    return res["fetched_questions"]


def __user_exists(user_id: str) -> bool:
    client = db_utils.connect()
    db = client.get_database(skill_config.DB_NAME)

    res = db.users.count_documents({"user_id": user_id})

    return res == 1


def __insert_new_user(user_id: str) -> None:
    client = db_utils.connect()
    db = client.get_database(skill_config.DB_NAME)

    db.users.insert_one({"user_id": user_id, "fetched_questions": []})
