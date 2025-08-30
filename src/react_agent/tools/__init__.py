from .base import Action, ActionArgument, Tool
from .registry import ToolRegistry
from .wikipedia import Wikipedia

TOOL_REGISTRY = ToolRegistry()
TOOL_REGISTRY.register(Wikipedia())


__all__ = ['Action', 'ActionArgument', 'Tool', 'Wikipedia', 'TOOL_REGISTRY']
