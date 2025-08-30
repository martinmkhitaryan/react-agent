import json

from .base import Tool
from .finish import Finish


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

        # NOTE: always register finish
        self.register(Finish())

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered.")

        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> Tool:
        return self._tools[name]

    def to_react_prompt(self) -> str:
        return json.dumps([tool.to_dict() for tool in self._tools.values()])
