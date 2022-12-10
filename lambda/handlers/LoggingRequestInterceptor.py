# encoding: utf-8
from ask_sdk_core.dispatch_components.request_components import (
    AbstractRequestInterceptor,
)
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils.request_util import get_intent_name, get_request_type
from utils import logger


class LoggingRequestInterceptor(AbstractRequestInterceptor):
    def process(self, handler_input: HandlerInput):
        attr = handler_input.attributes_manager.session_attributes or {}
        intent_received = "Unknown"
        user_state = attr.get("state", None)

        try:
            intent_received = get_intent_name(handler_input)
        except TypeError:
            intent_received = get_request_type(handler_input)

        logger.get_logger().info(
            f"Intent received: {intent_received}. User state: {user_state}"
        )
