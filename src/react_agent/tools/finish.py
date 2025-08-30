from .base import Action, ActionArgument, Tool


# TODO (low): Maybe think about better namings for the Finish, submit_answer and text.
class Finish(Tool):
    def __init__(self) -> str:
        super().__init__(
            name="Finish",
            description="Represents the final answer to the initial question, signaling that no further reasoning or actions are required.",
            actions=[
                Action(
                    name="submit_answer",
                    description="Submit the final answer to the initial question.",
                    arguments=[
                        ActionArgument(
                            name="text",
                            description="The final answer text.",
                        )
                    ],
                )
            ],
        )

    # NOTE: We can have pydantic models to validate input from the LLMs.
    def take_action(self, action_name: str, **kwargs) -> str:
        return getattr(self, f'_action_{action_name}')(**kwargs)

    def _action_submit_answer(self, **kwargs):
        return kwargs['text']
