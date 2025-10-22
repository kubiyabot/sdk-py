import inspect
from typing import Any, Dict, Callable

from kubiya.tools.models import Arg, Tool, Source


class FunctionTool(Tool):
    function: Callable

    @classmethod
    def from_function(cls, func: Callable, name: str, description: str, source: Source):
        signature = inspect.signature(func)

        type_mapping = {
            int: "int",
            str: "str",
            float: "float",
            bool: "bool",
            list: "array"
        }

        args = [
            Arg(
                name=param.name,
                type=type_mapping.get(param.annotation, "str") if param.annotation != inspect.Parameter.empty else "str",
                description=f"Parameter {param.name}",
                required=param.default == inspect.Parameter.empty,
            )
            for param in signature.parameters.values()
        ]

        return cls(
            name=name,
            description=description,
            type="python",
            args=args,
            source=source,
            function=func,
        )

    async def execute(self, args: Dict[str, Any]) -> Dict[str, Any]:
        return self.function(**args)
