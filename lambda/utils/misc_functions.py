# encoding: utf-8
from typing import Any, Dict, Union

from ask_sdk_model.slot import Slot
from utils.STATES import STATES


def parse_boolean_slot(slot_object: Slot):
    return (slot_object.value or "").lower() == "verdadero"


def initialize_attr(attr: Union[Dict[str, Any], None]) -> Dict[str, Any]:
    if attr is None:
        attr = {}

    attr["state"] = STATES["INITIALIZED"]

    return attr


def set_attr(attr: Union[Dict[str, Any], None], key: str, value: Any) -> Dict[str, Any]:
    if attr is None:
        attr = {}

    if not attr.get(key, False):
        attr[key] = value

    return attr
