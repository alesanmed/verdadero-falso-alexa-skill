# encoding: utf-8
from typing import Any, Dict

from ask_sdk_core.handler_input import HandlerInput
from connectors import db_functions
from i18n import i18nTexts
from utils.STATES import STATES


def new_question_process(handler_input: HandlerInput, texts: i18nTexts):
    attr = handler_input.attributes_manager.session_attributes or {}

    attr["state"] = STATES["QUESTION_ASKED"]

    question_obj = db_functions.retrieve_random_question(handler_input)

    attr["question_id"] = str(question_obj["_id"])

    handler_input.attributes_manager.session_attributes = attr

    speech_text = f"{question_obj['question']}. {texts.TRUE_FALSE_TEXT}"

    return speech_text


def check_correct_answer(question_obj: Dict[str, Any], user_answer: bool) -> bool:
    question_answer = question_obj["correct_answer"] == "True"

    return question_answer == user_answer
