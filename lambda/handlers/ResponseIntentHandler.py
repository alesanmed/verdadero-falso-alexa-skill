# encoding: utf-8
import random

from ask_sdk_core.dispatch_components.request_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils.predicate import is_intent_name
from ask_sdk_core.utils.request_util import get_slot
from ask_sdk_model.response import Response
from ask_sdk_model.ui.simple_card import SimpleCard
from connectors import db_functions
from utils import locale_functions, logger, misc_functions, question_functions
from utils.STATES import STATES


class ResponseIntentHandler(AbstractRequestHandler):
    """Handler for Answer Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        attr = handler_input.attributes_manager.session_attributes

        attr = misc_functions.set_attr(attr, "state", STATES["INITIALIZED"])

        handler_input.attributes_manager.session_attributes = attr

        return (
            is_intent_name("ResponseIntent")(handler_input)
            or is_intent_name("ResponseOnlyIntent")(handler_input)
        ) and attr.get("state") == STATES["QUESTION_ASKED"]

    def handle(self, handler_input: HandlerInput) -> Response:
        texts = locale_functions.get_locale_texts(handler_input)

        attr = handler_input.attributes_manager.session_attributes
        attr = misc_functions.initialize_attr(attr)

        attr["state"] = STATES["QUESTION_ANSWERED"]

        handler_input.attributes_manager.session_attributes = attr

        question_obj = db_functions.get_question(attr["question_id"])

        response_slot = get_slot(handler_input, "response")

        if response_slot is None:
            raise TypeError()

        user_answer = misc_functions.parse_boolean_slot(response_slot)

        logger.get_logger().info(f"ResponseIntentHandler user answer: {user_answer}")

        speech_text = ""

        if question_functions.check_correct_answer(question_obj, user_answer):
            speechcon = random.choice(texts.CORRECT_ANSWER_SPEECHCONS).capitalize()

            speech_text = f'<say-as interpret-as="interjection">{speechcon}</say-as>. '

            speech_text_card = f"{speechcon}. "
        else:
            speechcon = random.choice(texts.INCORRECT_ANSWER_SPEECHCONS).capitalize()

            speech_text = f'<say-as interpret-as="interjection">{speechcon}</say-as>, no es correcto. '

            speech_text_card = f"{speechcon}, no es correcto. "

        speech_text += f'{question_obj["more_info"]} {texts.NEW_ANSWER_TEXT}'

        speech_text_card += f'{question_obj["more_info"]} {texts.NEW_ANSWER_TEXT}'

        (
            handler_input.response_builder.speak(speech_text)
            .set_card(SimpleCard(texts.SKILL_NAME, speech_text_card))
            .ask(texts.NEW_ANSWER_TEXT)
        )

        return handler_input.response_builder.response
