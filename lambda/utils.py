import importlib
from db import db_functions

STATES = {
  'INITIALIZED': 0,
  'QUESTION_ASKED': 1,
  'QUESTION_ANSWERED': 2
}

def parse_boolean_slot(slot_value):
  return slot_value == 'verdadero'

def initialize_attr(attr):
  if not attr.get('state', False):
    attr['state'] = STATES['INITIALIZED']
  
  return attr

def new_question_process(handler_input, texts):
  attr = handler_input.attributes_manager.session_attributes
  attr['state'] = STATES['QUESTION_ASKED']

  question_obj = db_functions.retrieve_random_question(handler_input)

  attr['question_id'] = str(question_obj['_id'])

  handler_input.attributes_manager.session_attributes = attr

  speech_text = '{}, {}'.format(question_obj['question'], texts.TRUE_FALSE_TEXT)

  return speech_text

def check_correct_answer(question_obj, user_answer):
  return bool(question_obj['correct_answer']) == bool(user_answer)

def get_locale_texts(handler_input):
  return importlib.import_module('texts.{}'.format(
          __transform_locale(handler_input.request_envelope.request.locale)))

def __transform_locale(locale):
  return locale.replace('-', '_')