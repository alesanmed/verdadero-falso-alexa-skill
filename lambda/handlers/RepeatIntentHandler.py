# encoding: utf-8
from ask_sdk_core.dispatch_components.request_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils.predicate import is_intent_name
from ask_sdk_model.response import Response
from ask_sdk_model.ui.simple_card import SimpleCard
from connectors import db_functions
from utils import locale_functions
from utils.STATES import STATES


class RepeatIntentHandler(AbstractRequestHandler):
    """Handler for Repeat Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.RepeatIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        texts = locale_functions.get_locale_texts(handler_input)

        attr = handler_input.attributes_manager.session_attributes

        if attr is None:
            raise TypeError()

        question_obj = db_functions.get_question(attr["question_id"])

        speech_text = None

        if attr.get("state") == STATES["QUESTION_ASKED"]:
            speech_text = f'{question_obj["question"]}, {texts.TRUE_FALSE_TEXT}'
            (
                handler_input.response_builder.speak(speech_text)
                .set_card(SimpleCard(texts.SKILL_NAME, speech_text))
                .ask(texts.TRUE_FALSE_TEXT)
            )
        elif attr.get("state") == STATES["QUESTION_ANSWERED"]:
            speech_text = f'{question_obj["more_info"]}, {texts.NEW_ANSWER_TEXT}'
            (
                handler_input.response_builder.speak(speech_text)
                .set_card(SimpleCard(texts.SKILL_NAME, speech_text))
                .ask(texts.NEW_ANSWER_TEXT)
            )
        elif attr.get("state") == STATES["INITIALIZED"]:
            (
                handler_input.response_builder.speak(texts.HELLO_TEXT)
                .set_card(SimpleCard(texts.SKILL_NAME, texts.HELLO_TEXT))
                .ask(texts.HELLO_REPROMPT_TEXT)
            )

        return handler_input.response_builder.response
