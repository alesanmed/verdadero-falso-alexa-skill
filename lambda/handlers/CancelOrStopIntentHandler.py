# encoding: utf-8
from ask_sdk_core.dispatch_components.request_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils.predicate import is_intent_name
from ask_sdk_core.utils.request_util import get_slot
from ask_sdk_model.response import Response
from ask_sdk_model.ui.simple_card import SimpleCard
from utils import locale_functions, misc_functions
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

        user_doesnt_want_another_question = False

        # If the user already answered but says a response again, may be answering to the
        # question of getting a new question. So take that case into account
        if attr.get("state", None) == STATES["QUESTION_ANSWERED"]:
            if is_intent_name("AMAZON.NoIntent")(handler_input):
                user_doesnt_want_another_question = True
            elif is_intent_name("ResponseIntent")(handler_input) or is_intent_name(
                "ResponseOnlyIntent"
            )(handler_input):
                response_slot = get_slot(handler_input, "response")

                if response_slot is not None:
                    user_answer = misc_functions.parse_boolean_slot(response_slot)
                    user_doesnt_want_another_question = not user_answer

        return user_doesnt_want_another_question or is_cancel_or_stop_intent

    def handle(self, handler_input: HandlerInput) -> Response:
        texts = locale_functions.get_locale_texts(handler_input)

        (
            handler_input.response_builder.speak(texts.EXIT_TEXT)
            .set_card(SimpleCard(texts.SKILL_NAME, texts.EXIT_TEXT))
            .set_should_end_session(True)
        )

        return handler_input.response_builder.response
