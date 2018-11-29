# -*- coding: utf-8 -*-
from sys import path
import os
from os.path import dirname as dir

path.append(dir(path[0]))

from ask_sdk_model.slu.entityresolution.status_code import StatusCode

from utils.STATES import STATES
from utils import logger

def parse_boolean_slot(slot_object):
  resolutions = slot_object.resolutions.resolutions_per_authority

  resolution_id = None

  for resolution in resolutions:
    if resolution.status.code == StatusCode.ER_SUCCESS_MATCH:
      logger.get_logger().info('Resolution value: {}'.format(resolution.values[0]))
      resolution_id = resolution.values[0].value.id
      break

  if resolution_id != None:
    resolution_id = resolution_id == 'True'

  return resolution_id

def initialize_attr(attr):
  if not attr.get('state', False):
    attr['state'] = STATES['INITIALIZED']
  
  return attr