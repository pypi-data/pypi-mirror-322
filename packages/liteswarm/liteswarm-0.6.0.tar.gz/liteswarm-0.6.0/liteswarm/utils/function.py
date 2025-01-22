# Copyright 2025 GlyphyAI
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import inspect
from collections.abc import Callable
from enum import Enum
from typing import Any, Literal, get_type_hints

from griffe import Docstring, DocstringSectionKind

from liteswarm.types.agent import AgentTool
from liteswarm.types.utils import FunctionDocstring
from liteswarm.utils.logging import disable_logging, log_verbose

TYPE_MAP = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    list: "array",
    dict: "object",
    None: "null",
    Any: "object",
}


def tool_to_json(tool: AgentTool) -> dict[str, Any]:
    """Convert tool to OpenAI function schema.

    Creates a function schema from a tool's signature and docstring, handling
    both stateful and stateless tools. For stateful tools, skips the context
    parameter. Preserves parameter descriptions and type information.

    Args:
        tool: Tool to convert.

    Returns:
        OpenAI function schema as a dictionary.

    Raises:
        ValueError: If tool conversion fails.

    Examples:
        ```python
        @tool
        def fetch_weather(context: AgentContext[WeatherParams], city: str) -> str:
            '''Get weather for a city.

            Args:
                city: City name to fetch weather for.
            '''
            return context.params.service.fetch_weather(city)


        schema = tool_to_json(fetch_weather)
        # {
        #     "type": "function",
        #     "function": {
        #         "name": "fetch_weather",
        #         "description": "Get weather for a city.",
        #         "parameters": {
        #             "type": "object",
        #             "properties": {
        #                 "city": {
        #                     "type": "string",
        #                     "description": "City name to fetch weather for."
        #                 }
        #             },
        #             "required": ["city"]
        #         }
        #     }
        # }
        ```
    """  # noqa: D214
    try:
        signature = inspect.signature(tool.function)
        docstring = inspect.getdoc(tool.function) or ""
        type_hints = get_type_hints(tool.function)

        # Parse docstring
        func_docstring = parse_docstring_params(docstring)
        func_description = tool.description or func_docstring.description
        func_param_docs = func_docstring.parameters

        # Process parameters
        properties: dict[str, Any] = {}
        required: list[str] = []

        # For stateful tools, skip the first parameter (AgentContext)
        params_to_process = list(signature.parameters.items())
        if tool.has_context:
            params_to_process = params_to_process[1:]

        for param_name, param in params_to_process:
            # Skip *args and **kwargs
            if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                continue

            param_type = type_hints.get(param_name, type(Any))
            param_desc = func_param_docs.get(param_name, "")

            # Build parameter schema
            param_schema: dict[str, Any] = {
                "type": TYPE_MAP.get(param_type, "string"),
                "description": param_desc if param_desc else f"Parameter: {param_name}",
            }

            # Handle enums
            if isinstance(param_type, type) and issubclass(param_type, Enum):
                param_schema["type"] = "string"
                param_schema["enum"] = [e.value for e in param_type]

            properties[param_name] = param_schema

            # Add to required if no default value
            if param.default == param.empty:
                required.append(param_name)

        schema: dict[str, Any] = {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": func_description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                },
            },
        }

        if required:
            schema["function"]["parameters"]["required"] = required

        return schema

    except Exception as e:
        log_verbose(f"Failed to convert tool {tool.name}: {str(e)}", level="ERROR")
        raise ValueError(f"Failed to convert tool {tool.name}: {str(e)}") from e


def tools_to_json(tools: list[AgentTool] | None) -> list[dict[str, Any]] | None:
    """Convert multiple tools to OpenAI function schemas.

    Converts a list of tools to their function schema representations.
    Returns None if input is None to support optional tool lists.

    Args:
        tools: List of tools to convert.

    Returns:
        List of function schemas, or None if input is None.

    Examples:
        ```python
        tools = [fetch_weather, calculate_sum]
        schemas = tools_to_json(tools)
        # [
        #     {"type": "function", "function": {...}},  # fetch_weather
        #     {"type": "function", "function": {...}},  # calculate_sum
        # ]
        ```
    """
    if not tools:
        return None

    return [tool_to_json(tool) for tool in tools]


def parse_docstring_params(docstring: str) -> FunctionDocstring:
    """Parse function docstring into structured format.

    Uses Griffe to extract description and parameter documentation
    from docstrings in various styles (Google, Sphinx, NumPy).

    Args:
        docstring: Raw docstring text to parse.

    Returns:
        Structured docstring information.

    Examples:
        Google style:
            ```python
            def example(name: str) -> str:
                \"\"\"Greet someone.

                Args:
                    name: Person to greet.

                Returns:
                    Greeting message.
                \"\"\"
                return f"Hello {name}"

            info = parse_docstring_params(example.__doc__)
            # info.description = "Greet someone."
            # info.parameters = {"name": "Person to greet."}
            ```

        Sphinx style:
            ```python
            def example(name: str) -> str:
                \"\"\"Greet someone.

                :param name: Person to greet.
                :return: Greeting message.
                \"\"\"
                return f"Hello {name}"

            info = parse_docstring_params(example.__doc__)
            # Same structured output
            ```
    """  # noqa: D214
    if not docstring:
        return FunctionDocstring()

    try:
        with disable_logging():
            style = detect_docstring_style(docstring)
            docstring_parser = Docstring(docstring)
            parsed_docstring = docstring_parser.parse(parser=style)

        description = ""
        parameters: dict[str, str] = {}

        for section in parsed_docstring:
            match section.kind:
                case DocstringSectionKind.text:
                    section_dict = section.as_dict()
                    description = section_dict.get("value", "")

                case DocstringSectionKind.parameters:
                    section_dict = section.as_dict()
                    param_list = section_dict.get("value", [])

                    for param in param_list:
                        param_name = getattr(param, "name", None)
                        param_desc = getattr(param, "description", "")
                        if param_name:
                            parameters[param_name] = param_desc

                case _:
                    continue

        return FunctionDocstring(
            description=description,
            parameters=parameters,
        )

    except Exception as e:
        log_verbose(f"Failed to parse docstring: {e}", level="WARNING")
        return FunctionDocstring()


def detect_docstring_style(docstring: str) -> Literal["google", "sphinx", "numpy"]:
    """Detect docstring format using pattern matching.

    Analyzes docstring content to determine its style based on
    common patterns and section markers.

    Args:
        docstring: Raw docstring text to analyze.

    Returns:
        Detected style: "google", "sphinx", or "numpy".

    Examples:
        Google style detection:
            ```python
            style = detect_docstring_style(\"\"\"
                Do something.

                Args:
                    x: Input value.

                Returns:
                    Modified value.
            \"\"\")
            assert style == "google"
            ```

        Sphinx style detection:
            ```python
            style = detect_docstring_style(\"\"\"
                Do something.

                :param x: Input value.
                :return: Modified value.
            \"\"\")
            assert style == "sphinx"
            ```
    """  # noqa: D214
    if not docstring:
        return "google"  # default to google style

    # Google style indicators
    if "Args:" in docstring or "Returns:" in docstring or "Raises:" in docstring:
        return "google"

    # Sphinx style indicators
    if ":param" in docstring or ":return:" in docstring or ":rtype:" in docstring:
        return "sphinx"

    # NumPy style indicators
    if (
        "Parameters\n" in docstring
        or "Returns\n" in docstring
        or "Parameters\r\n" in docstring
        or "Returns\r\n" in docstring
    ):
        return "numpy"

    return "google"


def function_has_parameter(func: Callable[..., Any], param: str) -> bool:
    """Check if function accepts specific parameter.

    Inspects function's type hints to determine if it accepts
    the given parameter name.

    Args:
        func: Function to inspect.
        param: Parameter name to check.

    Returns:
        True if parameter exists, False otherwise.

    Examples:
        Parameter check:
            ```python
            def greet(name: str) -> str:
                return f"Hello {name}"


            assert function_has_parameter(greet, "name")
            assert not function_has_parameter(greet, "age")
            ```

        Type hints required:
            ```python
            def greet(name):  # No type hint
                return f"Hello {name}"


            # Returns False (no type hints)
            result = function_has_parameter(greet, "name")
            ```
    """
    return param in get_type_hints(func)
