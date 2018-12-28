# -*- coding: utf-8 -*-
from sys import path
import os
from os.path import dirname as dir

path.append(dir(path[0]))

from utils.STATES import STATES
from connectors import db_functions

def new_question_process(handler_input, texts):
  attr = handler_input.attributes_manager.session_attributes
  attr['state'] = STATES['QUESTION_ASKED']

  question_obj = db_functions.retrieve_random_question(handler_input)

  attr['question_id'] = str(question_obj['_id'])

  handler_input.attributes_manager.session_attributes = attr

  speech_text = '{}. {}'.format(question_obj['question'], texts.TRUE_FALSE_TEXT)

  return speech_text

def check_correct_answer(question_obj, user_answer):
  question_answer = question_obj['correct_answer'] == 'True'
  
  return question_answer == user_answer