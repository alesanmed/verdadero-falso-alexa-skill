# -*- coding: utf-8 -*-
from sys import path
import os
from os.path import dirname as dir

path.append(dir(path[0]))

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model.ui import SimpleCard
from utils import locale_functions, misc_functions, question_functions
from utils.STATES import STATES

class GetNewQuestionIntentHandler(AbstractRequestHandler):
    """Handler for Get New Question Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr = handler_input.attributes_manager.session_attributes

        attr = misc_functions.initialize_attr(attr)

        handler_input.attributes_manager.session_attributes = attr

        user_wants_another_question = (
            attr['state'] == STATES['QUESTION_ANSWERED'] and
            is_intent_name("AMAZON.YesIntent")(handler_input)
        )

        return (is_intent_name("GetNewQuestionIntent")(handler_input) or 
                user_wants_another_question)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        texts = locale_functions.get_locale_texts(handler_input)

        speech_text = question_functions.new_question_process(handler_input, texts)

        (handler_input.response_builder
            .speak(speech_text)
            .set_card(SimpleCard(texts.SKILL_NAME, speech_text))
            .ask(speech_text))

        return handler_input.response_builder.response