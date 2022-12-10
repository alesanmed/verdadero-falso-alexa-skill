# encoding: utf-8
from ask_sdk_core.dispatch_components.request_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils.predicate import is_intent_name
from ask_sdk_model.response import Response
from ask_sdk_model.ui.simple_card import SimpleCard
from utils import locale_functions
from utils.STATES import STATES


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:

        attr = handler_input.attributes_manager.session_attributes

        if attr is None:
            return False

        is_cancel_or_stop_intent = is_intent_name("AMAZON.CancelIntent")(
            handler_input
        ) or is_intent_name("AMAZON.StopIntent")(handler_input)

        user_doesnt_want_another_question = attr.get("state") == STATES[
            "QUESTION_ANSWERED"
        ] and is_intent_name("AMAZON.NoIntent")(handler_input)

        return user_doesnt_want_another_question or is_cancel_or_stop_intent

    def handle(self, handler_input: HandlerInput) -> Response:
        texts = locale_functions.get_locale_texts(handler_input)

        (
            handler_input.response_builder.speak(texts.EXIT_TEXT)
            .set_card(SimpleCard(texts.SKILL_NAME, texts.EXIT_TEXT))
            .set_should_end_session(True)
        )

        return handler_input.response_builder.response
