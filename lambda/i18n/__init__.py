from dataclasses import dataclass
from typing import List


@dataclass
class i18nTexts:
    SKILL_NAME: str
    HELP_TEXT: str
    EXIT_TEXT: str
    EXCEPTION_TEXT: str
    EXCEPTION_REPROMPT_TEXT: str
    HELLO_TEXT: str
    HELLO_REPROMPT_TEXT: str
    TRUE_FALSE_TEXT: str
    CORRECT_ANSWER_SPEECHCONS: List[str]
    INCORRECT_ANSWER_SPEECHCONS: List[str]
    NEW_ANSWER_TEXT: str
    START_OVER_TEXT: str
