from contextlib import contextmanager
from typing import Generator

from rasa.dialogue_understanding.constants import (
    RASA_RECORD_COMMANDS_AND_PROMPTS_ENV_VAR_NAME,
)
from rasa.utils.common import get_bool_env_variable

record_commands_and_prompts = get_bool_env_variable(
    RASA_RECORD_COMMANDS_AND_PROMPTS_ENV_VAR_NAME, False
)


@contextmanager
def set_record_commands_and_prompts() -> Generator:
    global record_commands_and_prompts
    record_commands_and_prompts = True
    try:
        yield
    finally:
        record_commands_and_prompts = False
