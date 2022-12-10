# encoding: utf-8
from ask_sdk_core.dispatch_components.request_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils.predicate import is_intent_name
from ask_sdk_model.response import Response
from ask_sdk_model.ui.simple_card import SimpleCard
from utils import locale_functions


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        texts = locale_functions.get_locale_texts(handler_input)

        (
            handler_input.response_builder.speak(texts.HELP_TEXT)
            .set_card(SimpleCard(texts.SKILL_NAME, texts.HELP_TEXT))
            .ask(texts.HELLO_REPROMPT_TEXT)
        )

        return handler_input.response_builder.response
