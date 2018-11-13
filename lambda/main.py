# -*- coding: utf-8 -*-

import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestInterceptor
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

from db import db_functions
import utils

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
        texts = utils.get_locale_texts(handler_input)
        
        attr = handler_input.attributes_manager.session_attributes

        attr['state'] = utils.STATES['INITIALIZED']

        handler_input.attributes_manager.session_attributes = attr
        
        handler_input.response_builder.speak(texts.HELLO_TEXT).ask(texts.HELLO_REPROMPT_TEXT)
        
        return handler_input.response_builder.response


class GetNewQuestionIntentHandler(AbstractRequestHandler):
    """Handler for Get New Question Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr = handler_input.attributes_manager.session_attributes

        attr = utils.initialize_attr(attr)

        handler_input.attributes_manager.session_attributes = attr

        user_wants_another_question = (
            attr['state'] == utils.STATES['QUESTION_ANSWERED'] and
            is_intent_name("AMAZON.YesIntent")(handler_input)
        )

        return (is_intent_name("GetNewQuestionIntent")(handler_input) or 
                user_wants_another_question)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        texts = utils.get_locale_texts(handler_input)

        speech_text = utils.new_question_process(handler_input, texts)

        handler_input.response_builder.speak(speech_text).ask(speech_text)

        return handler_input.response_builder.response

class QuestionAnswerIntentHandler(AbstractRequestHandler):
    """Handler for Answer Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr = handler_input.attributes_manager.session_attributes

        attr = utils.initialize_attr(attr)

        handler_input.attributes_manager.session_attributes = attr

        return (is_intent_name("QuestionAnswerIntent")(handler_input) and 
                attr['state'] == utils.STATES['QUESTION_ASKED'])

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        texts = utils.get_locale_texts(handler_input)
        
        attr = handler_input.attributes_manager.session_attributes
        attr['state'] = utils.STATES['QUESTION_ANSWERED']

        handler_input.attributes_manager.session_attributes = attr

        question_obj = db_functions.get_question(attr['question_id'])

        slots = handler_input.request_envelope.request.intent.slots
        
        user_answer = utils.parse_boolean_slot(slots.get("response").value)

        logger.info('QuestionAnswerIntentHandler user answer: {}'.format(user_answer))

        speech_text = ''
        
        if utils.check_correct_answer(question_obj, user_answer):
            speech_text += texts.CORRECT_ANSWER_TEXT
        else:
            speech_text += texts.INCORRECT_ANSWER_TEXT

        speech_text += '{}. {}'.format(question_obj['more_info'], texts.NEW_ANSWER_TEXT)

        handler_input.response_builder.speak(speech_text).ask(texts.NEW_ANSWER_TEXT)

        return handler_input.response_builder.response

class RepeatIntentHandler(AbstractRequestHandler):
    """Handler for Repeat Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.RepeatIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        texts = utils.get_locale_texts(handler_input)
        
        attr = handler_input.attributes_manager.session_attributes

        question_obj = db_functions.get_question(attr['question_id'])

        speech_text = None

        if attr['state'] == utils.STATES['QUESTION_ASKED']:
            speech_text = '{}, {}'.format(question_obj['question'], texts.TRUE_FALSE_TEXT)
            handler_input.response_builder.speak(
                speech_text).ask(texts.TRUE_FALSE_TEXT)
        elif attr['state'] == utils.STATES['QUESTION_ANSWERED']:
            speech_text = '{}, {}'.format(question_obj['more_info'], texts.NEW_ANSWER_TEXT)
            handler_input.response_builder.speak(
                speech_text).ask(texts.NEW_ANSWER_TEXT)
        elif attr['state'] == utils.STATES['INITIALIZED']:
            handler_input.response_builder.speak(texts.HELLO_TEXT).ask(texts.HELLO_REPROMPT_TEXT)

        return handler_input.response_builder.response

class StartOverIntentHandler(AbstractRequestHandler):
    """Handler for Start Over Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.StartOverIntent")(handler_input)

    def handle(self, handler_input):
        texts = utils.get_locale_texts(handler_input)

        speech_text = '{} {}, {}'.format(texts.START_OVER_TEXT,
                                        utils.new_question_process(handler_input, texts),
                                        texts.TRUE_FALSE_TEXT)

        handler_input.response_builder.speak(speech_text).ask(texts.TRUE_FALSE_TEXT)

        return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        texts = utils.get_locale_texts(handler_input)

        speech_text = texts.HELP_TEXT

        handler_input.response_builder.speak(
            speech_text)

        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool        
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        attr = handler_input.attributes_manager.session_attributes

        is_cancel_or_stop_intent = (is_intent_name("AMAZON.CancelIntent")(handler_input) or 
                                    is_intent_name("AMAZON.StopIntent")(handler_input))
        
        user_doesnt_want_another_question = (attr['state'] == utils.STATES['QUESTION_ANSWERED'] and 
                                            is_intent_name("AMAZON.NoIntent")(handler_input))
        
        return user_doesnt_want_another_question or is_cancel_or_stop_intent
                

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        texts = utils.get_locale_texts(handler_input)

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
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        logger.info('SessionEndedRequestHandler: Session end requested. handler_input:\n{}'.format(
            handler_input.request_envelope.request))
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

        texts = utils.get_locale_texts(handler_input)

        handler_input.response_builder.speak(texts.EXCEPTION_TEXT)

        return handler_input.response_builder.response

class LoggingRequestInterceptor(AbstractRequestInterceptor):
    def process(self, handler_input):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        attr = handler_input.attributes_manager.session_attributes
        intent_received = 'Unknown'

        logger.info('Request: {}'.format(handler_input.request_envelope))

        if handler_input.request_envelope.request.object_type == 'IntentRequest':
            intent_received = handler_input.request_envelope.request.intent.name
        else:
            intent_received = handler_input.request_envelope.request.object_type

        logger.info('Intent received: {}'.format(intent_received))
        logger.info('User state: {}'.format(attr.get('state', None)))

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

sb.add_global_request_interceptor(LoggingRequestInterceptor())

handler = sb.lambda_handler()