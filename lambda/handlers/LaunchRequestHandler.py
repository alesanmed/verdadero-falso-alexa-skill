# -*- coding: utf-8 -*-
from sys import path
import os
from os.path import dirname as dir

path.append(dir(path[0]))

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model.ui import SimpleCard
from utils import locale_functions
from utils.STATES import STATES

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        texts = locale_functions.get_locale_texts(handler_input)
        
        attr = handler_input.attributes_manager.session_attributes

        attr['state'] = STATES['INITIALIZED']

        handler_input.attributes_manager.session_attributes = attr
        
        (handler_input
                    .response_builder
                    .speak(texts.HELLO_TEXT)
                    .set_card(SimpleCard(texts.SKILL_NAME, texts.HELLO_TEXT))
                    .ask(texts.HELLO_REPROMPT_TEXT))
        
        return handler_input.response_builder.response