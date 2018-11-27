# -*- coding: utf-8 -*-
from sys import path
import os
from os.path import dirname as dir

path.append(dir(path[0]))

from utils.STATES import STATES

def parse_boolean_slot(slot_value):
  return slot_value == 'verdadero'

def initialize_attr(attr):
  if not attr.get('state', False):
    attr['state'] = STATES['INITIALIZED']
  
  return attr