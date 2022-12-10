# encoding: utf-8
from ask_sdk_core.dispatch_components.exception_components import (
    AbstractExceptionHandler,
)
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.response import Response
from ask_sdk_model.ui.simple_card import SimpleCard
from utils import locale_functions, logger


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input: HandlerInput, exception: Exception) -> bool:
        return True

    def handle(self, handler_input: HandlerInput, exception: Exception) -> Response:
        logger.get_logger().error(exception, exc_info=True)

        texts = locale_functions.get_locale_texts(handler_input)

        (
            handler_input.response_builder.speak(texts.EXCEPTION_TEXT)
            .set_card(SimpleCard(texts.SKILL_NAME, texts.EXCEPTION_TEXT))
            .ask(texts.EXCEPTION_REPROMPT_TEXT)
        )

        return handler_input.response_builder.response
