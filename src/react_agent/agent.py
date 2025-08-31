import json
from typing import Iterable

from google import genai
from google.genai.types import GenerateContentConfig
from google.oauth2 import service_account

from .settings import (
    PROMPT_EXAMPLES_PATH,
    PROMPT_TEMPLATE_PATH,
    VERTEXAI_CREDENTIALS_PATH,
    VERTEXAI_LOCATION,
    VERTEXAI_PROJECT_ID,
)
from .tools import TOOL_REGISTRY

TOOLS_REACT_PROMPT = TOOL_REGISTRY.to_react_prompt()


class ReactAgent:
    def __init__(self, model_name: str = "gemini-2.5-flash") -> None:
        self._model_name = model_name

        credentials = service_account.Credentials.from_service_account_file(
            VERTEXAI_CREDENTIALS_PATH, scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )

        self._genai_client = genai.Client(
            credentials=credentials,
            vertexai=True,
            project=VERTEXAI_PROJECT_ID,
            location=VERTEXAI_LOCATION,
        )

    def react(self, query: str) -> str:
        prompt = self._build_initial_prompt(query)

        for i in range(1, 5):  # NOTE: Add max retries to settings.
            print(prompt)

            # NOTE: Currently making two separate LLM calls, one to generate a Thought, and another to generate an Action.
            # I think it can be optimized by modifying the prompt to ask the LLM to return both the Thought and Action together in a single call.
            # For example:
            # {
            #   "thought": "I need to retrieve weather data to answer the question.",
            #   "action": { "tool": "weather_api", "input": "New York" }
            # }
            # This eliminates the need for a second call and avoids potential mismatch or drift between Thought and Action steps.

            thought = (
                self._ask_llm(prompt + f"\nThought {i}:", stop_sequences=["\n"]).strip().removeprefix(f"Thought {i}")
            )

            if f"Action {i}:" in thought:
                error_feedback = (
                    "Error: Your previous Thought included an Action JSON, which is not allowed. "
                    "A Thought should contain only human-readable reasoning and intentions. "
                    "Please rewrite the Thought correctly, without any Action JSON."
                )
                thought_prompt_with_feedback = prompt + "\n" + error_feedback
                thought = (
                    self._ask_llm(thought_prompt_with_feedback, stop_sequences=["\n"])
                    .strip()
                    .removeprefix(f"Thought {i}")
                )

            action = (
                self._ask_llm(prompt + f"\nThought {i}: {thought}\nAction {i}:", stop_sequences=["\n"])
                .strip()
                .removeprefix(f"nAction {i}")
            )
            print(f"Action {i}: {action}")

            # TODO: Try to return both thought and action in one prompt, like its done in the research paper.
            # thought_and_action = self._ask_llm(prompt + f"\nThought {i}:", stop_sequences=[f"\nObservation {i}:"])
            # try:
            #     thought, action = thought_and_action.strip().split(f"\nAction {i}: ")
            # except ValueError:
            #     thought = thought_and_action.strip().split('\n')[0]
            #     action = self._ask_llm(prompt + f"\nThought {i}: {thought}\nAction {i}:", stop_sequences=["\n"]).strip()

            observation, is_finished = self._execute_action(action)
            print(f"Observation {i}: {observation}")

            step = f"Thought {i}: {thought}\nAction {i}: {action}\nObservation {i}: {observation}\n"
            prompt += step

            if is_finished:
                print(f'Answer: {observation}')
                break

        return prompt

    def _build_initial_prompt(self, query: str) -> str:
        template = open(PROMPT_TEMPLATE_PATH).read()
        return template.format(
            tools=TOOLS_REACT_PROMPT,
            current_query=query if query.startswith("Question:") else f"Question: {query}",
        )

    def _execute_action(self, action: str) -> tuple[str, bool]:
        try:
            action_data = json.loads(action)
            tool = TOOL_REGISTRY.get_tool(action_data["tool"])
            result = tool.take_action(action_data["action"], **action_data["args"])
            return (result, tool.name == 'Finish')
        except json.JSONDecodeError:
            return (f"Error: Invalid JSON format in action: {action}", False)
        except KeyError as e:
            return (f"Error: Missing required field in action: {e}", False)
        except Exception as e:
            return (f"Error executing action: {e}", False)

    def _ask_llm(self, prompt: str, stop_sequences: Iterable[str] = ["\n"]) -> str:
        # TODO: Later integrate pydantic settings and make it more flexible to change the model conig.
        response = self._genai_client.models.generate_content(
            model=self._model_name,
            contents=prompt,
            config=GenerateContentConfig(
                top_p=1,
                temperature=0.0,
                max_output_tokens=512,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop_sequences=stop_sequences,
                # system_instruction TODO: Check if passing instructions directly is better then using a simple template, should it also contain examples or not, etc ... # noqa
            ),
        )
        return response.text
