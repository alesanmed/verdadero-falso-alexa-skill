# encoding: utf-8
import inspect
import os
from importlib import import_module

from ask_sdk_core.dispatch_components.exception_components import (
    AbstractExceptionHandler,
)
from ask_sdk_core.dispatch_components.request_components import (
    AbstractRequestHandler,
    AbstractRequestInterceptor,
)
from ask_sdk_core.skill_builder import SkillBuilder
from connectors import db_utils
from utils import logger

logger.init_logger()

db_utils.connect()

sb = SkillBuilder()

base_path = os.path.join(os.path.dirname(__file__), "handlers")
files = os.listdir(base_path)

for file_name in files:
    handler, _ = os.path.splitext(file_name)

    if handler.startswith("__"):
        continue

    HandlerClass = getattr(import_module(f"handlers.{handler}"), handler)
    handler_parent_classes = inspect.getmro(HandlerClass)

    logger.get_logger().info(f"Adding {handler} to SkillBuilder")

    if AbstractRequestHandler in handler_parent_classes:
        sb.add_request_handler(HandlerClass())
    elif AbstractExceptionHandler in handler_parent_classes:
        sb.add_exception_handler(HandlerClass())
    elif AbstractRequestInterceptor in handler_parent_classes:
        sb.add_global_request_interceptor(HandlerClass())

logger.get_logger().info("Added all handlers to SkillBuilder")

lambda_handler = sb.lambda_handler()
