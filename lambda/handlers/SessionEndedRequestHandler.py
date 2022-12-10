# encoding: utf-8
from ask_sdk_core.dispatch_components.request_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils.predicate import is_request_type
from ask_sdk_model.response import Response
from utils import logger


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        logger.get_logger().info(
            f"SessionEndedRequestHandler: Session end requested. handler_input:\n{handler_input.request_envelope.request}"
        )

        return handler_input.response_builder.response
