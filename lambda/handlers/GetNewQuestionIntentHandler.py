# encoding: utf-8
from ask_sdk_core.dispatch_components.request_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils.predicate import is_intent_name
from ask_sdk_core.utils.request_util import get_slot
from ask_sdk_model.response import Response
from ask_sdk_model.ui.simple_card import SimpleCard
from utils import locale_functions, misc_functions, question_functions
from utils.STATES import STATES


class GetNewQuestionIntentHandler(AbstractRequestHandler):
    """Handler for Get New Question Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        attr = handler_input.attributes_manager.session_attributes

        attr = misc_functions.set_attr(attr, "state", STATES["INITIALIZED"])

        handler_input.attributes_manager.session_attributes = attr

        user_wants_another_question = False

        # If the user already answered but says a response again, may be answering to the
        # question of getting a new question. So take that case into account
        if attr.get("state", None) == STATES["QUESTION_ANSWERED"]:
            if is_intent_name("AMAZON.YesIntent")(handler_input):
                user_wants_another_question = True
            elif is_intent_name("ResponseIntent")(handler_input) or is_intent_name(
                "ResponseOnlyIntent"
            )(handler_input):
                response_slot = get_slot(handler_input, "response")

                if response_slot is not None:
                    user_answer = misc_functions.parse_boolean_slot(response_slot)
                    user_wants_another_question = user_answer

        return (
            is_intent_name("GetNewQuestionIntent")(handler_input)
            or user_wants_another_question
        )

    def handle(self, handler_input: HandlerInput) -> Response:
        texts = locale_functions.get_locale_texts(handler_input)

        speech_text = question_functions.new_question_process(handler_input, texts)

        (
            handler_input.response_builder.speak(speech_text)
            .set_card(SimpleCard(texts.SKILL_NAME, speech_text))
            .ask(speech_text)
        )

        return handler_input.response_builder.response
