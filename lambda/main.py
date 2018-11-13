# -*- coding: utf-8 -*-

import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

from db import db_functions
from utils import get_locale_texts, STATES, check_correct_answer, new_question_process

import importlib
import datetime

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        texts = get_locale_texts(handler_input)
        
        handler_input.response_builder.speak(texts.HELLO_TEXT)
        
        return handler_input.response_builder.response


class GetNewQuestionIntentHandler(AbstractRequestHandler):
    """Handler for Get New Question Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr = handler_input.attributes_manager.session_attributes

        user_wants_another_question = (
            attr['state'] == STATES['QUESTION_ANSWERED'] and
            is_intent_name("AMAZON.YesIntent")
        )

        return (is_intent_name("GetNewQuestionIntent")(handler_input) or 
                user_wants_another_question)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        texts = get_locale_texts(handler_input)

        speech_text = '{}, {}'.format(new_question_process(handler_input, texts), texts.TRUE_FALSE_TEXT)

        handler_input.response_builder.speak(speech_text)

        return handler_input.response_builder.response

class QuestionAnswerIntentHandler(AbstractRequestHandler):
    """Handler for Answer Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("QuestionAnswerIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        texts = get_locale_texts(handler_input)
        
        attr = handler_input.attributes_manager.session_attributes
        attr['state'] = STATES['QUESTION_ASWERED']

        question_obj = db_functions.get_question(attr['question_id'])

        user_answer = handler_input.request_envelope['intent']['slots']['response']['value']

        speech_text = ''
        
        if check_correct_answer(question_obj, user_answer):
            speech_text += texts.CORRECT_ANSWER_TEXT
        else:
            speech_text += texts.INCORRECT_ANSWER_TEXT

        speech_text += question_obj['more_info']

        handler_input.response_builder.speak(
            speech_text)

        handler_input.response_builder.speak(texts.NEW_ANSWER_TEXT)

        return handler_input.response_builder.response

class RepeatIntentHandler(AbstractRequestHandler):
    """Handler for Repeat Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.RepeatIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        texts = get_locale_texts(handler_input)
        
        attr = handler_input.attributes_manager.session_attributes

        question_obj = db_functions.get_question(attr['question_id'])

        speech_text = None

        if attr['state'] == STATES['QUESTION_ASKED']:
            speech_text = '{}, {}'.format(question_obj['question'], texts.TRUE_FALSE_TEXT)
        elif attr['state'] == STATES['QUESTION_ANSWERED']:
            speech_text = '{}, {}'.format(question_obj['more_info'], texts.NEW_ANSWER_TEXT)

        handler_input.response_builder.speak(
            speech_text)

        return handler_input.response_builder.response

class StartOverIntentHandler(AbstractRequestHandler):
    """Handler for Start Over Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.StartOverIntent")(handler_input)

    def handle(self, handler_input):
        texts = get_locale_texts(handler_input)

        speech_text = '{} {}, {}'.format(texts.START_OVER_TEXT,
                                        new_question_process(handler_input, texts),
                                        texts.TRUE_FALSE_TEXT)

        handler_input.response_builder.speak(speech_text)

        return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        texts = get_locale_texts(handler_input)

        speech_text = texts.HELP_TEXT

        handler_input.response_builder.speak(
            speech_text)

        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr = handler_input.attributes_manager.session_attributes

        is_cancel_or_stop_intent = (is_intent_name("AMAZON.CancelIntent")(handler_input) or 
                                    is_intent_name("AMAZON.StopIntent")(handler_input))
        
        user_doesnt_want_another_question = (attr['state'] == 'ANSWERED' and 
                                            is_intent_name("AMAZON.NoIntent")(handler_input))
        
        return is_cancel_or_stop_intent or user_doesnt_want_another_question
                

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        texts = get_locale_texts(handler_input)

        speech_text = texts.EXIT_TEXT

        handler_input.response_builder.speak(speech_text)
        
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        pass


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        texts = get_locale_texts(handler_input)

        handler_input.response_builder.speak(texts.EXCEPTION_TEXT)

        return handler_input.response_builder.response

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetNewQuestionIntentHandler())
sb.add_request_handler(QuestionAnswerIntentHandler())
sb.add_request_handler(RepeatIntentHandler())
sb.add_request_handler(StartOverIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()