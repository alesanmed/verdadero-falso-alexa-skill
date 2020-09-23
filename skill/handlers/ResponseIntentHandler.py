# -*- coding: utf-8 -*-
from sys import path
import os
from os.path import dirname as dir

path.append(dir(path[0]))

import random

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model.ui import SimpleCard

from utils import locale_functions, misc_functions, question_functions, logger
from utils.STATES import STATES
from connectors import db_functions

class ResponseIntentHandler(AbstractRequestHandler):
    """Handler for Answer Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr = handler_input.attributes_manager.session_attributes

        attr = misc_functions.initialize_attr(attr)

        handler_input.attributes_manager.session_attributes = attr

        return ((is_intent_name("ResponseIntent")(handler_input) or 
                is_intent_name("ResponseOnlyIntent")(handler_input)) and 
                attr.get('state') == STATES['QUESTION_ASKED'])

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        texts = locale_functions.get_locale_texts(handler_input)
        
        attr = handler_input.attributes_manager.session_attributes
        attr['state'] = STATES['QUESTION_ANSWERED']

        handler_input.attributes_manager.session_attributes = attr

        question_obj = db_functions.get_question(attr['question_id'])

        slots = handler_input.request_envelope.request.intent.slots
        
        user_answer = misc_functions.parse_boolean_slot(slots.get("response"))

        logger.get_logger().info('ResponseIntentHandler user answer: {}'.format(user_answer))

        speech_text = ''
        
        if question_functions.check_correct_answer(question_obj, user_answer):
            speech_text = '<say-as interpret-as="interjection">{}</say-as>. '.format(
                random.choice(texts.CORRECT_ANSWER_SPEECHCONS))
            
            speech_text_card = '{}. '.format(
                random.choice(texts.CORRECT_ANSWER_SPEECHCONS))
        else:
            speech_text = '<say-as interpret-as="interjection">{}</say-as>, no es correcto. '.format(
                random.choice(texts.INCORRECT_ANSWER_SPEECHCONS))
            
            speech_text_card = '{}, no es correcto. '.format(
                random.choice(texts.INCORRECT_ANSWER_SPEECHCONS))

        speech_text += '{}. {}'.format(question_obj['more_info'], texts.NEW_ANSWER_TEXT)
        speech_text_card += '{}. {}'.format(question_obj['more_info'], texts.NEW_ANSWER_TEXT)

        (handler_input.response_builder
                .speak(speech_text)
                .set_card(SimpleCard(texts.SKILL_NAME, speech_text_card))
                .ask(texts.NEW_ANSWER_TEXT))

        return handler_input.response_builder.response