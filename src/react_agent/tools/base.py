import abc
from dataclasses import asdict, dataclass


@dataclass(frozen=True, kw_only=True)
class ActionArgument:
    name: str
    description: str

    # NOTE: Research later
    # type?: str
    # examples?: list[str]


@dataclass(frozen=True, kw_only=True)
class Action:
    name: str
    description: str
    arguments: list[ActionArgument]


class Tool(abc.ABC):
    def __init__(self, name: str, description: str, actions: list[Action]) -> None:
        self.name = name
        self.description = description
        self.actions = actions

    # NOTE: We can have pydantic models to validate input from the LLMs.
    @abc.abstractmethod
    def take_action(self, action_name: str, **kwargs) -> str:
        raise NotImplementedError

    def to_dict(self) -> dict:
        return {
            "tool_name": self.name,
            "description": self.description,
            "actions": [asdict(action) for action in self.actions],
        }
