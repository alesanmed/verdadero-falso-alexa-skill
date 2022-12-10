# encoding: utf-8
import importlib

from ask_sdk_core.handler_input import HandlerInput
from i18n import i18nTexts


def get_locale_texts(handler_input: HandlerInput) -> i18nTexts:
    request = handler_input.request_envelope.request
    locale = "es_ES"

    if request is not None and request.locale is not None:
        locale = request.locale

    lang_code = __transform_locale(locale)
    module = importlib.import_module(f"i18n.{lang_code}")

    class_obj: i18nTexts = getattr(module, f"{lang_code}Texts")

    return class_obj


def __transform_locale(locale: str) -> str:
    return locale.replace("-", "_")
