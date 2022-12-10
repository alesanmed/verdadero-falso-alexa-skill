# encoding: utf-8
from ask_sdk_core.dispatch_components.request_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils.predicate import is_intent_name
from ask_sdk_model.response import Response
from ask_sdk_model.ui.simple_card import SimpleCard
from utils import locale_functions, question_functions


class StartOverIntentHandler(AbstractRequestHandler):
    """Handler for Start Over Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("AMAZON.StartOverIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        texts = locale_functions.get_locale_texts(handler_input)

        speech_text = f"{texts.START_OVER_TEXT} {question_functions.new_question_process(handler_input, texts)}"

        (
            handler_input.response_builder.speak(speech_text)
            .set_card(SimpleCard(texts.SKILL_NAME, speech_text))
            .ask(texts.TRUE_FALSE_TEXT)
        )

        return handler_input.response_builder.response
