# Copyright 2025 GlyphyAI
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import inspect
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any, Concatenate, Self, cast, final, get_args, get_origin, overload

from pydantic.dataclasses import dataclass
from typing_extensions import override

from liteswarm.types.agent import (
    Agent,
    AgentContext,
    AgentOutput,
    AgentSwitch,
    AgentTool,
    ContextParams,
    ToolParams,
)
from liteswarm.types.llm import Message
from liteswarm.types.typing import _None, _NoneType, is_subtype, validate_value

ToolFuncStatelessSync = Callable[ToolParams, Any]
"""Synchronous tool function without context access.

Function that takes only tool-specific parameters and returns a result
synchronously. Used for simple operations that don't need context.

Example:
    ```python
    def add(a: int, b: int) -> int:
        return a + b
    ```
"""

ToolFuncStatelessAsync = Callable[ToolParams, Awaitable[Any]]
"""Asynchronous tool function without context access.

Function that takes only tool-specific parameters and returns a result
asynchronously. Used for I/O operations that don't need context.

Example:
    ```python
    async def fetch_data(url: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()
    ```
"""

ToolFuncStatefulSync = Callable[Concatenate[AgentContext[ContextParams, AgentOutput], ToolParams], Any]
"""Synchronous tool function with context access.

Function that takes agent context and tool-specific parameters, returns
result synchronously. Used when tool needs access to conversation state.

Example:
    ```python
    def get_user_data(
        context: AgentContext[UserParams, None],
        field: str,
    ) -> Any:
        return getattr(context.params.user, field)
    ```
"""

ToolFuncStatefulAsync = Callable[Concatenate[AgentContext[ContextParams, AgentOutput], ToolParams], Awaitable[Any]]
"""Asynchronous tool function with context access.

Function that takes agent context and tool-specific parameters, returns
result asynchronously. Used for I/O operations that need context.

Example:
    ```python
    async def fetch_user_data(
        context: AgentContext[UserParams, None],
        endpoint: str,
    ) -> dict:
        return await context.params.client.get(endpoint)
    ```
"""

ToolFuncStateless = ToolFuncStatelessSync[ToolParams] | ToolFuncStatelessAsync[ToolParams]
"""Union type for stateless tool functions.

Represents either a sync or async function that doesn't require context.
Used as a type constraint for tools that operate independently.

Example:
    ```python
    # Can be either sync
    def calculate(x: int) -> int: ...

    # Or async
    async def fetch(url: str) -> str: ...
    ```
"""

ToolFuncStateful = (
    ToolFuncStatefulSync[ContextParams, AgentOutput, ToolParams]
    | ToolFuncStatefulAsync[ContextParams, AgentOutput, ToolParams]
)
"""Union type for stateful tool functions.

Represents either a sync or async function that requires context.
Used as a type constraint for context-aware tools.

Example:
    ```python
    # Can be either sync
    def get_history(context: AgentContext[Params, Output]) -> list[str]: ...

    # Or async
    async def update_state(context: AgentContext[Params, Output], data: dict) -> None: ...
    ```
"""

ToolFunc = (
    ToolFuncStatefulSync[ContextParams, AgentOutput, ToolParams]
    | ToolFuncStatefulAsync[ContextParams, AgentOutput, ToolParams]
    | ToolFuncStatelessSync[ToolParams]
    | ToolFuncStatelessAsync[ToolParams]
)
"""Union type for all possible tool functions.

Represents any valid tool function type, whether stateful/stateless or sync/async.
Used as the main type constraint for tool implementations.

Example:
    ```python
    # Can be any of:
    def simple_sync(x: int) -> int: ...
    async def simple_async(url: str) -> str: ...
    def context_sync(context: AgentContext[P, O], data: dict) -> None: ...
    async def context_async(context: AgentContext[P, O], query: str) -> list[str]: ...
    ```
"""


@final
@dataclass
class Tool(AgentTool[ContextParams, AgentOutput, ToolParams]):
    """Wrapper for tool functions with type safety.

    Implements the AgentTool protocol with complete type checking and
    execution handling. Supports both stateful/stateless and sync/async
    tool functions while maintaining type information.

    Args:
        function: Tool implementation function.
        name: Name for agent to reference tool.
        description: Optional description for agent.
        params_type: Expected context parameter type.
        has_context: Whether function needs context.
        is_async: Whether function is async.

    Examples:
        Stateless tool:
            ```python
            tool = Tool(
                function=add,
                name="add",
                description="Add two numbers",
                has_context=False,
            )
            ```

        Stateful async tool:
            ```python
            tool = Tool(
                function=fetch_user_data,
                name="fetch_user_data",
                description="Fetch user data from API",
                params_type=UserParams,
                has_context=True,
                is_async=True,
            )
            ```

    Notes:
        - Validates parameter types at runtime
        - Handles both sync and async execution
        - Supports context-aware and stateless tools
        - Used internally by Agent for tool management
    """

    function: ToolFunc[ContextParams, AgentOutput, ToolParams]
    """Underlying tool implementation."""

    name: str
    """Name used by agents to reference this tool."""

    description: str | None
    """Human-readable description of tool's purpose and usage."""

    params_type: type[ContextParams] = _NoneType
    """Expected type for context parameters in context-aware tools."""

    has_context: bool = True
    """Whether tool receives context as first argument."""

    is_async: bool = False
    """Whether tool is implemented as an async function."""

    @override
    async def run(
        self,
        context: AgentContext[ContextParams, AgentOutput],
        *args: ToolParams.args,
        **kwargs: ToolParams.kwargs,
    ) -> Any:
        """Execute tool with given context and arguments.

        Handles both stateful and stateless execution, managing async
        operations automatically.

        Args:
            context: Current agent context.
            *args: Positional arguments for tool.
            **kwargs: Keyword arguments for tool.

        Returns:
            Tool execution result.

        Raises:
            TypeError: If parameter types don't match.
        """
        if self.has_context:
            return await self._run_stateful(context, *args, **kwargs)
        return await self._run_stateless(*args, **kwargs)

    async def _run_stateful(
        self,
        context: AgentContext[ContextParams, AgentOutput],
        *args: ToolParams.args,
        **kwargs: ToolParams.kwargs,
    ) -> Any:
        """Execute a stateful tool with context.

        Internal method to handle execution of context-aware tools,
        managing both sync and async variants.

        Args:
            context: Current agent context.
            *args: Tool positional arguments.
            **kwargs: Tool keyword arguments.

        Returns:
            Tool execution result.

        Raises:
            TypeError: If context params don't match required type.
        """
        if self.params_type and not validate_value(context.params, self.params_type):
            raise TypeError(
                f"Tool {self.name} requires context params type {self.params_type}, but got {type(context.params)}"
            )

        func = cast(ToolFuncStateful[ContextParams, AgentOutput, ToolParams], self.function)
        if self.is_async:
            return await func(context, *args, **kwargs)
        else:
            return func(context, *args, **kwargs)

    async def _run_stateless(
        self,
        *args: ToolParams.args,
        **kwargs: ToolParams.kwargs,
    ) -> Any:
        """Execute a stateless tool without context.

        Internal method to handle execution of context-free tools,
        managing both sync and async variants.

        Args:
            *args: Tool positional arguments.
            **kwargs: Tool keyword arguments.

        Returns:
            Tool execution result.
        """
        func = cast(ToolFuncStateless[ToolParams], self.function)
        if self.is_async:
            return await func(*args, **kwargs)
        else:
            return func(*args, **kwargs)


@final
@dataclass
class ToolResult:
    """Result of a tool execution.

    Contains the tool's output and optional agent switch request.
    Used to both return data and request agent switches when needed.

    Args:
        content: Text content of result.
        agent_switch: Optional agent switch request.

    Examples:
        Simple result:
            ```python
            return ToolResult(content="Operation completed")
            ```

        With agent switch:
            ```python
            return ToolResult.switch_to(
                expert_agent,
                content="Switching to expert",
                params=ExpertParams(domain="physics"),
            )
            ```

    Notes:
        - Used as return type for all tools
        - Supports agent switching through AgentSwitch
        - Content is always converted to string
    """

    content: str
    """Text content of the result."""

    agent_switch: AgentSwitch | None = None
    """Optional request to switch to another agent."""

    @classmethod
    def switch_to(
        cls,
        agent: Agent[ContextParams, AgentOutput],
        content: str | None = None,
        params: ContextParams = _None,
        messages: list[Message] | None = None,
    ) -> Self:
        """Create result with agent switch.

        Convenience method to create a result that includes an agent
        switch request.

        Args:
            agent: Agent to switch to.
            content: Result content.
            params: Parameters for new agent.
            messages: Optional new message history.

        Returns:
            ToolResult configured for agent switch.
        """
        return cls(
            content=content or f"<switched to {agent.id}>",
            agent_switch=AgentSwitch(
                agent=agent,
                messages=messages,
                params=params,
            ),
        )


ToolBuilder = Callable[
    [ToolFuncStateful[ContextParams, AgentOutput, ToolParams]],
    Tool[ContextParams, AgentOutput, ToolParams],
]
"""Type for tool decorator factory with context.

Function type for creating tool decorators that wrap context-aware
functions. Used internally by the @tool decorator.

Example:
    ```python
    @tool(params_type=MyParams)
    def my_tool(context: AgentContext[MyParams, None], data: str) -> str:
        return f"Processing {data} for {context.params.user}"
    ```
"""

ToolBuilderPlain = Callable[
    [ToolFuncStateless[ToolParams]],
    Tool[Any, Any, ToolParams],
]
"""Type for tool decorator factory without context.

Function type for creating tool decorators that wrap context-free
functions. Used internally by the @tool_plain decorator.

Example:
    ```python
    @tool_plain
    def simple_tool(x: int, y: int) -> int:
        return x + y
    ```
"""


def _wrap_stateful_tool(
    *,
    agent: Agent[ContextParams, AgentOutput] | None = None,
    params_type: type[ContextParams] = _NoneType,
    output_type: type[AgentOutput] = _NoneType,
    name: str | None = None,
    description: str | None = None,
) -> ToolBuilder[ContextParams, AgentOutput, ToolParams]:
    """Create a decorator for context-aware tool functions.

    Internal factory function that creates decorators for wrapping
    functions into Tool objects with context access.

    Args:
        agent: Optional agent to attach tool to.
        params_type: Expected context parameter type.
        output_type: Expected output type.
        name: Override for tool name.
        description: Override for tool description.

    Returns:
        Decorator function for creating Tool objects.
    """

    def decorator(
        func: ToolFuncStateful[ContextParams, AgentOutput, ToolParams],
    ) -> Tool[ContextParams, AgentOutput, ToolParams]:
        @wraps(func)
        def wrapper(context: AgentContext[ContextParams, AgentOutput], *args: Any, **kwargs: Any) -> Any:
            return func(context, *args, **kwargs)

        tool_params_type = agent.params_type if agent else params_type
        tool_obj = Tool[ContextParams, AgentOutput, ToolParams](
            function=wrapper,
            name=name or func.__name__,
            description=description or func.__doc__,
            params_type=tool_params_type,
            has_context=True,
            is_async=inspect.iscoroutinefunction(func),
        )

        if agent:
            agent.tools.append(tool_obj)

        return tool_obj

    return decorator


def _wrap_stateful_tool_dynamic(
    func: ToolFuncStateful[ContextParams, AgentOutput, ToolParams],
) -> Tool[ContextParams, AgentOutput, ToolParams]:
    """Create Tool object from context-aware function.

    Internal function that wraps a context-aware function into a Tool
    object, inferring type information from function signature.

    Args:
        func: Context-aware function to wrap.

    Returns:
        Tool object configured for context access.

    Raises:
        TypeError: If context parameter is not properly annotated.
    """

    @wraps(func)
    def wrapper(
        context: AgentContext[ContextParams, AgentOutput],
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        return func(context, *args, **kwargs)

    params = list(inspect.signature(func).parameters.values())
    if not params:
        raise ValueError("Function must have at least one parameter")

    context_param = params[0]
    context_type = context_param.annotation

    # Handle no annotation case
    if context_type == inspect.Parameter.empty:
        return Tool(
            function=wrapper,
            name=func.__name__,
            description=func.__doc__,
            params_type=_NoneType,
            has_context=True,
            is_async=inspect.iscoroutinefunction(func),
        )

    # Get the base type (handles generics)
    base_type = get_origin(context_type) or context_type

    # Check if it's AgentContext (either raw or generic)
    if not (base_type == AgentContext or is_subtype(base_type, AgentContext)):
        raise TypeError(f"First parameter must be annotated with AgentContext, got {context_type}")

    # Extract params_type from generic args if present
    type_args = get_args(context_type)
    params_type = type_args[0] if type_args else _NoneType

    return Tool(
        function=wrapper,
        name=func.__name__,
        description=func.__doc__,
        params_type=params_type,
        has_context=True,
        is_async=inspect.iscoroutinefunction(func),
    )


@overload
def tool(
    func: ToolFuncStateful[ContextParams, AgentOutput, ToolParams],
) -> Tool[ContextParams, AgentOutput, ToolParams]: ...


@overload
def tool(
    *,
    agent: Agent[ContextParams, AgentOutput],
    name: str | None = None,
    description: str | None = None,
) -> ToolBuilder[ContextParams, AgentOutput, ToolParams]: ...


@overload
def tool(
    *,
    params_type: type[ContextParams] = _NoneType,
    output_type: type[AgentOutput] = _NoneType,
    name: str | None = None,
    description: str | None = None,
) -> ToolBuilder[ContextParams, AgentOutput, ToolParams]: ...


def tool(
    func: ToolFuncStateful[ContextParams, AgentOutput, ToolParams] | None = None,
    *,
    agent: Agent[ContextParams, AgentOutput] | None = None,
    params_type: type[ContextParams] = _NoneType,
    output_type: type[AgentOutput] = _NoneType,
    name: str | None = None,
    description: str | None = None,
) -> Tool[ContextParams, AgentOutput, ToolParams] | ToolBuilder[ContextParams, AgentOutput, ToolParams]:
    """Decorator for creating context-aware tools.

    Wraps functions into Tool objects that have access to agent context.
    Can be used as a simple decorator or with configuration parameters.

    Args:
        func: Function to wrap.
        agent: Optional agent to attach tool to.
        params_type: Expected context parameter type.
        output_type: Expected output type.
        name: Override for tool name.
        description: Override for tool description.

    Returns:
        Tool object or decorator function.

    Examples:
        Simple usage:
            ```python
            @tool
            def get_data(context: AgentContext[MyParams, None], query: str) -> str:
                return context.params.db.query(query)
            ```

        With configuration:
            ```python
            @tool(
                agent=my_agent,
                params_type=MyParams,
                name="fetch_data",
            )
            def get_data(context: AgentContext[MyParams, None], query: str) -> str:
                return context.params.db.query(query)
            ```
    """
    if func is None:
        return _wrap_stateful_tool(
            agent=agent,
            params_type=params_type,
            output_type=output_type,
            name=name,
            description=description,
        )

    return _wrap_stateful_tool_dynamic(func)


def _wrap_stateless_tool(
    *,
    agent: Agent[ContextParams, AgentOutput] | None = None,
    params_type: type[ContextParams] = _None,
    output_type: type[AgentOutput] = _None,
    name: str | None = None,
    description: str | None = None,
) -> ToolBuilderPlain[ToolParams]:
    """Create a decorator for context-free tool functions.

    Internal factory function that creates decorators for wrapping
    functions into Tool objects without context access.

    Args:
        agent: Optional agent to attach tool to.
        params_type: Expected context parameter type.
        output_type: Expected output type.
        name: Override for tool name.
        description: Override for tool description.

    Returns:
        Decorator function for creating Tool objects.
    """

    def decorator(
        func: ToolFuncStateless[ToolParams],
    ) -> Tool[Any, Any, ToolParams]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        tool_params_type = agent.params_type if agent else params_type
        tool_obj = Tool[Any, Any, ToolParams](
            function=wrapper,
            name=name or func.__name__,
            description=description or func.__doc__,
            params_type=tool_params_type,
            has_context=False,
            is_async=inspect.iscoroutinefunction(func),
        )

        if agent:
            agent.tools.append(tool_obj)

        return tool_obj

    return decorator


def _wrap_stateless_tool_dynamic(
    func: ToolFuncStateless[ToolParams],
) -> Tool[Any, Any, ToolParams]:
    """Create Tool object from context-free function.

    Internal function that wraps a context-free function into a Tool
    object with no context access requirements.

    Args:
        func: Context-free function to wrap.

    Returns:
        Tool object configured for stateless execution.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    return Tool(
        function=wrapper,
        name=func.__name__,
        description=func.__doc__,
        params_type=_NoneType,
        has_context=False,
        is_async=inspect.iscoroutinefunction(func),
    )


@overload
def tool_plain(
    func: ToolFuncStateless[ToolParams],
) -> Tool[Any, Any, ToolParams]: ...


@overload
def tool_plain(
    *,
    agent: Agent[ContextParams, AgentOutput],
    name: str | None = None,
    description: str | None = None,
) -> ToolBuilderPlain[ToolParams]: ...


@overload
def tool_plain(
    *,
    params_type: type[ContextParams] = _NoneType,
    output_type: type[AgentOutput] = _NoneType,
    name: str | None = None,
    description: str | None = None,
) -> ToolBuilderPlain[ToolParams]: ...


def tool_plain(
    func: ToolFuncStateless[ToolParams] | None = None,
    *,
    agent: Agent[ContextParams, AgentOutput] | None = None,
    params_type: type[ContextParams] = _NoneType,
    output_type: type[AgentOutput] = _NoneType,
    name: str | None = None,
    description: str | None = None,
) -> Tool[Any, Any, ToolParams] | ToolBuilderPlain[ToolParams]:
    """Decorator for creating context-free tools.

    Wraps functions into Tool objects that operate independently
    without access to agent context. Can be used as a simple
    decorator or with configuration parameters.

    Args:
        func: Function to wrap.
        agent: Optional agent to attach tool to.
        params_type: Expected context parameter type.
        output_type: Expected output type.
        name: Override for tool name.
        description: Override for tool description.

    Returns:
        Tool object or decorator function.

    Examples:
        Simple usage:
            ```python
            @tool_plain
            def add(a: int, b: int) -> int:
                return a + b
            ```

        With configuration:
            ```python
            @tool_plain(
                agent=my_agent,
                name="multiply",
                description="Multiply two numbers",
            )
            def mul(a: int, b: int) -> int:
                return a * b
            ```
    """
    if func is None:
        return _wrap_stateless_tool(
            agent=agent,
            params_type=params_type,
            output_type=output_type,
            name=name,
            description=description,
        )

    return _wrap_stateless_tool_dynamic(func)
