import importlib

STATES = {
  'QUESTION_ASKED': 0,
  'QUESTION_ANSWERED': 1
}

def get_locale_texts(handler_input):
  return importlib.import_module('texts.{}'.format(
          __transform_locale(handler_input.request_envelope.request.locale)))


def __transform_locale(locale):
  return locale.replace('-', '_')