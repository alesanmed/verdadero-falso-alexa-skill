# encoding: utf-8
from ask_sdk_core.dispatch_components.request_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils.predicate import is_request_type
from ask_sdk_model.response import Response
from ask_sdk_model.ui.simple_card import SimpleCard
from utils import locale_functions, misc_functions


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        texts = locale_functions.get_locale_texts(handler_input)

        attr = handler_input.attributes_manager.session_attributes

        attr = misc_functions.initialize_attr(attr)

        handler_input.attributes_manager.session_attributes = attr

        (
            handler_input.response_builder.speak(texts.HELLO_TEXT)
            .set_card(SimpleCard(texts.SKILL_NAME, texts.HELLO_TEXT))
            .ask(texts.HELLO_REPROMPT_TEXT)
        )

        return handler_input.response_builder.response
