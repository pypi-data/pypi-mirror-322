# Copyright 2025 GlyphyAI
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from abc import abstractmethod
from collections.abc import Callable
from enum import Enum
from typing import Any, Generic, final

import orjson
from pydantic import Field, field_serializer, model_validator
from pydantic.dataclasses import dataclass
from typing_extensions import ParamSpec, TypeVar

from liteswarm.types.llm import LLM, Message
from liteswarm.types.typing import _NoneType, validate_type, validate_value

ContextParams = TypeVar("ContextParams", default=Any)
"""Type variable for context parameters."""

AgentOutput = TypeVar("AgentOutput", default=Any)
"""Type variable for agent output type."""

ToolParams = ParamSpec("ToolParams", default=...)
"""Type variable for parameter specification."""


class AgentState(str, Enum):
    """State of an agent in the conversation lifecycle.

    Tracks an agent's readiness and activity status during execution.
    State transitions occur automatically during processing based on
    tool calls and response completion.

    States:
        IDLE: Agent is ready for new tasks
        ACTIVE: Agent is processing a task
        STALE: Agent needs replacement

    Notes:
        - IDLE -> ACTIVE: When agent starts processing
        - ACTIVE -> STALE: After response or tool calls complete
        - STALE: Triggers agent switching if available
    """

    IDLE = "idle"
    """Agent is ready for new tasks."""

    ACTIVE = "active"
    """Agent is processing a task."""

    STALE = "stale"
    """Agent needs replacement."""


@dataclass
class AgentTool(Generic[ContextParams, AgentOutput, ToolParams]):
    """Protocol for tool functions available to agents.

    Base class for tools that can be called by agents during execution.
    Maintains type information and execution context for proper tool
    invocation and result handling.

    Args:
        function: Underlying tool implementation
        name: Tool name for agent reference
        description: Optional tool description
        params_type: Expected context parameter type
        has_context: Whether tool requires context
        is_async: Whether tool is async

    Notes:
        - Validates parameter types against context
        - Handles both sync and async execution
        - Supports stateful and stateless tools
    """

    function: Callable[..., Any]
    """Underlying tool implementation."""

    name: str
    """Tool name for agent reference."""

    description: str | None
    """Optional tool description."""

    params_type: type[ContextParams]
    """Expected context parameter type."""

    has_context: bool
    """Whether tool requires context."""

    is_async: bool
    """Whether tool is async."""

    @abstractmethod
    async def run(
        self,
        context: "AgentContext[ContextParams, AgentOutput]",
        *args: ToolParams.args,
        **kwargs: ToolParams.kwargs,
    ) -> Any:
        """Execute the tool with given context and arguments."""
        raise NotImplementedError

    @field_serializer("function")
    def serialize_function(
        self,
        function: Callable[..., Any],
    ) -> str:
        return str(function)

    @field_serializer("params_type")
    def serialize_params_type(
        self,
        params_type: type[ContextParams],
    ) -> str:
        return str(params_type)


@final
@dataclass
class AgentContext(Generic[ContextParams, AgentOutput]):
    """Complete execution state for an agent run.

    Maintains the complete state needed for agent execution, including
    configuration, parameters, and message history. Used throughout the
    execution lifecycle to track conversation state and context.

    Args:
        agent: Agent configuration and state.
        params: Context parameters for dynamic resolution.
        messages: Complete message history.

    Examples:
        Basic context:
            ```python
            context = AgentContext(
                agent=agent,
                params=None,
                messages=[Message(role="user", content="Hello")],
            )
            ```

        With typed parameters:
            ```python
            @dataclass
            class MyParams:
                user_name: str
                task: str


            context = AgentContext(
                agent=agent,
                params=MyParams(user_name="Alice", task="coding"),
                messages=messages,
            )
            ```

    Notes:
        - Validates parameter types against agent's params_type
        - Serializes parameters for logging and debugging
        - Used internally by Swarm for execution control
    """

    agent: "Agent[ContextParams, AgentOutput]"
    """Agent configuration and state."""

    params: ContextParams
    """Context parameters for dynamic resolution."""

    messages: list[Message]
    """Complete message history."""

    @model_validator(mode="after")
    def validate_params(self) -> "AgentContext[ContextParams, AgentOutput]":
        if not validate_value(self.params, self.agent.params_type):
            raise TypeError(
                f"Params type {type(self.params)} does not match expected type {self.agent.params_type}",
            )
        return self

    @field_serializer("params")
    def serialize_params(self, params: ContextParams) -> str:
        try:
            return orjson.dumps(params).decode()
        except Exception:
            return str(params)


@final
@dataclass
class AgentSwitch(Generic[ContextParams, AgentOutput]):
    """Configuration for switching between agents.

    Used during agent switching to specify the new agent configuration
    and optionally override the execution context. Provides flexibility
    in maintaining or replacing message history during switching.

    Args:
        agent: Agent to switch to.
        params: Parameters for the new agent.
        messages: Optional message history override.

    Examples:
        Switch with new history:
            ```python
            switch = AgentSwitch(
                agent=expert_agent,
                params=ExpertParams(domain="physics"),
                messages=[Message(role="user", content="New context")],
            )
            ```

        Preserve history:
            ```python
            switch = AgentSwitch(
                agent=expert_agent,
                params=ExpertParams(domain="physics"),
                messages=None,  # Keep current history
            )
            ```

    Notes:
        - If messages is None, current history is preserved
        - Validates parameter types against new agent's params_type
        - Used by tools to request agent switch
    """

    agent: "Agent[ContextParams, AgentOutput]"
    """Agent to switch to."""

    params: ContextParams
    """Parameters for the new agent."""

    messages: list[Message] | None = None
    """Optional message history override."""

    @model_validator(mode="after")
    def validate_params(self) -> "AgentSwitch[ContextParams, AgentOutput]":
        if not validate_value(self.params, self.agent.params_type):
            raise TypeError(
                f"Params type {type(self.params)} does not match expected type {self.agent.params_type}",
            )
        return self

    @field_serializer("params")
    def serialize_params(self, params: ContextParams) -> str:
        try:
            return orjson.dumps(params).decode()
        except Exception:
            return str(params)


AgentInstructionsBuilder = Callable[[AgentContext[ContextParams, AgentOutput]], str]
"""Function type for dynamic instruction generation.

Takes an agent context and returns instruction string. Used to create
context-aware instructions that can incorporate runtime information.

Example:
    ```python
    def build_instructions(context: AgentContext[MyParams, None]) -> str:
        return f"You are helping {context.params.user_name} with {context.params.task}."
    ```
"""

AgentInstructions = str | AgentInstructionsBuilder[ContextParams, AgentOutput]
"""Type for agent instructions.

Can be either a static string or a dynamic builder function. Static strings
are used directly, while builder functions are called with context to generate
instructions.

Example:
    ```python
    # Static instructions
    instructions: AgentInstructions = "You are a helpful assistant."

    # Dynamic instructions
    instructions: AgentInstructions = lambda ctx: f"Help {ctx.params.user_name}"
    ```
"""

AgentOutputParserStateless = Callable[[str], AgentOutput]
"""Function type for parsing agent output without context.

Takes raw output string and returns parsed result. Used when parsing
doesn't require access to agent context.

Example:
    ```python
    def parse_json(content: str) -> dict:
        return json.loads(content)
    ```
"""

AgentOutputParserStateful = Callable[[AgentContext[ContextParams, AgentOutput], str], AgentOutput]
"""Function type for context-aware output parsing.

Takes agent context and raw output string, returns parsed result.
Used when parsing needs access to runtime context.

Example:
    ```python
    def parse_with_context(
        context: AgentContext[MyParams, MyOutput],
        content: str,
    ) -> MyOutput:
        return MyOutput(
            user=context.params.user_name,
            result=content,
        )
    ```
"""

AgentOutputParser = AgentOutputParserStateful[ContextParams, AgentOutput] | AgentOutputParserStateless[AgentOutput]
"""Type for agent output parsers.

Can be either a stateless function that only needs the output string,
or a stateful function that also requires context access.

Example:
    ```python
    # Stateless parser
    parser: AgentOutputParser = json.loads

    # Stateful parser
    parser: AgentOutputParser = lambda ctx, out: MyOutput(user=ctx.params.user, result=out)
    ```
"""


@final
@dataclass
class Agent(Generic[ContextParams, AgentOutput]):
    """Configuration for an AI conversation participant.

    Defines an agent's identity, behavior, and capabilities through
    instructions and language model settings. Supports dynamic instruction
    generation and structured output parsing.

    Args:
        id: Unique identifier for the agent.
        instructions: Static text or dynamic instruction builder.
        llm: Language model configuration.
        params_type: Expected context parameter type.
        output_type: Expected output type.
        output_parser: Optional output parsing function.
        tools: List of available tools.

    Examples:
        Basic agent:
            ```python
            agent = Agent(
                id="assistant",
                instructions="You are a helpful assistant.",
                llm=LLM(model="gpt-4o"),
            )
            ```

        With dynamic instructions:
            ```python
            def get_instructions(context: AgentContext[MyParams, None]) -> str:
                return f"Help {context.params.user_name} with {context.params.task}."


            agent = Agent(
                id="expert",
                instructions=get_instructions,
                llm=LLM(model="gpt-4o"),
                params_type=MyParams,
            )
            ```

        With structured output:
            ```python
            @dataclass
            class CodeResponse:
                code: str
                explanation: str


            agent = Agent(
                id="coder",
                instructions="Generate code based on requirements.",
                llm=LLM(
                    model="gpt-4o",
                    response_format=CodeResponse,
                ),
                output_type=CodeResponse,
            )
            ```

    Notes:
        - Supports both static and dynamic instructions
        - Validates parameter and output types
        - Manages tool availability and execution
        - Tracks agent state for lifecycle management
    """

    id: str
    """Unique identifier for the agent."""

    instructions: AgentInstructions[ContextParams, AgentOutput]
    """Static text or dynamic instruction builder."""

    llm: LLM
    """Language model configuration."""

    params_type: type[ContextParams] = _NoneType
    """Expected context parameter type."""

    output_type: type[AgentOutput] = _NoneType
    """Expected output type."""

    output_parser: AgentOutputParser[ContextParams, AgentOutput] | None = None
    """Optional output parsing function."""

    tools: list[AgentTool[ContextParams, Any]] = Field(default_factory=list)
    """Tools available to the agent."""

    state: AgentState = Field(default=AgentState.IDLE, init=False)
    """Current execution state."""

    @model_validator(mode="after")
    def validate_tools(self) -> "Agent[ContextParams, AgentOutput]":
        """Validate that all tools have matching params_type."""
        for tool in self.tools:
            if not validate_type(tool.params_type, self.params_type):
                raise TypeError(
                    f"Tool {tool.name} params_type {tool.params_type} does not match agent params_type {self.params_type}"
                )

        return self

    @field_serializer("instructions")
    def serialize_instructions(
        self,
        instructions: "AgentInstructions[ContextParams, AgentOutput]",
    ) -> str:
        """Serialize agent instructions."""
        return str(instructions) if callable(instructions) else instructions

    @field_serializer("params_type")
    def serialize_params_type(
        self,
        params_type: type[ContextParams] | None,
    ) -> str:
        """Serialize agent params_type."""
        return str(params_type) if params_type else "None"

    @field_serializer("output_type")
    def serialize_output_type(
        self,
        output_type: type[AgentOutput] | None,
    ) -> str:
        """Serialize agent output_type."""
        return str(output_type) if output_type else "None"

    @field_serializer("output_parser")
    def serialize_output_parser(
        self,
        output_parser: Callable[..., AgentOutput] | None,
    ) -> str:
        """Serialize agent output_parser."""
        return str(output_parser) if output_parser else "None"

    @property
    def is_active(self) -> bool:
        """Whether the agent is currently processing.

        Returns:
            True if agent is in ACTIVE state, False otherwise.
        """
        return self.state == AgentState.ACTIVE

    @property
    def is_stale(self) -> bool:
        """Whether the agent needs replacement.

        Returns:
            True if agent is in STALE state, False otherwise.
        """
        return self.state == AgentState.STALE

    def activate(self) -> None:
        """Mark agent as active for processing.

        Transitions agent to ACTIVE state, indicating it's currently
        handling a request. Called automatically by Swarm before
        processing begins.
        """
        self.state = AgentState.ACTIVE

    def invalidate(self) -> None:
        """Mark agent as needing replacement.

        Transitions agent to STALE state, indicating it should be
        replaced if possible. Called automatically after response
        completion or tool calls.
        """
        self.state = AgentState.STALE
