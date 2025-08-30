# TODO: Later integrate pydantic settings and make it more flexible to change the model conig for example.
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
PROMPTS_DIR = BASE_DIR / "prompts"
PROMPT_TEMPLATE_PATH = PROMPTS_DIR / "hotpot_qa_template.txt"
PROMPT_EXAMPLES_PATH = PROMPTS_DIR / "examples" / 'hotpotqa.json'


VERTEXAI_CREDENTIALS_PATH = os.environ["VERTEXAI_CREDENTIALS_PATH"]
assert VERTEXAI_CREDENTIALS_PATH, "First set VERTEXAI_CREDENTIALS_PATH env variable"

VERTEXAI_PROJECT_ID = os.environ["VERTEXAI_PROJECT_ID"]
assert VERTEXAI_PROJECT_ID, "First set VERTEXAI_PROJECT_ID env variable"

VERTEXAI_LOCATION = os.environ["VERTEXAI_LOCATION"]
assert VERTEXAI_LOCATION, "First set VERTEXAI_LOCATION env variable"
