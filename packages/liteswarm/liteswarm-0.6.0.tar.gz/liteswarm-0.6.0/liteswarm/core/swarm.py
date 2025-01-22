# Copyright 2025 GlyphyAI
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import asyncio
import sys
import uuid
from collections import deque
from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING, Any

import litellm
import orjson
from litellm import CustomStreamWrapper
from litellm.exceptions import ContextWindowExceededError
from litellm.types.utils import ChatCompletionDeltaToolCall, ModelResponse, StreamingChoices
from litellm.utils import token_counter
from pydantic import BaseModel
from typing_extensions import TypeVar

from liteswarm.core.swarm_stream import SwarmStream
from liteswarm.types.agent import Agent, AgentContext, AgentOutput, ContextParams
from liteswarm.types.collections import AsyncStream, ReturnItem, YieldItem, returnable
from liteswarm.types.events import (
    AgentCompleteEvent,
    AgentResponseChunkEvent,
    AgentResponseEvent,
    AgentRunCompleteEvent,
    AgentRunStartEvent,
    AgentStartEvent,
    AgentSwitchEvent,
    CompletionResponseChunkEvent,
    SwarmEvent,
    ToolCallResultEvent,
)
from liteswarm.types.exceptions import (
    CompletionError,
    ContextLengthError,
    MaxAgentSwitchesError,
    MaxResponseContinuationsError,
    SwarmError,
)
from liteswarm.types.llm import (
    Delta,
    Message,
    ResponseFormat,
    ResponseFormatJsonSchema,
    ResponseSchema,
    Usage,
)
from liteswarm.types.swarm import (
    AgentIterationResult,
    AgentResponse,
    AgentResponseChunk,
    AgentResponseResult,
    AgentRunResult,
    CompletionResponseChunk,
    ResponseCost,
    ToolCallResult,
)
from liteswarm.types.tools import AgentSwitch, ToolResult
from liteswarm.types.typing import _None, is_subtype
from liteswarm.utils.function import tools_to_json
from liteswarm.utils.logging import log_verbose
from liteswarm.utils.messages import dump_messages, get_max_tokens
from liteswarm.utils.misc import (
    parse_agent_output,
    parse_content,
    parse_partial_response,
    resolve_agent_instructions,
    safe_get_attr,
)
from liteswarm.utils.retry import retry_wrapper
from liteswarm.utils.usage import calculate_response_cost

if TYPE_CHECKING:
    from liteswarm.types.typing import JSON


litellm.modify_params = True

FinalContextParams = TypeVar("FinalContextParams", default=Any)
"""Type variable for context type."""

FinalOutputType = TypeVar("FinalOutputType", default=Any)
"""Type variable for response format type."""


class Swarm:
    """Provider-agnostic runtime client for AI agent execution.

    Swarm is a lightweight, stateless runtime client that executes agent interactions
    with LLMs. It provides the core execution engine for agent operations, including
    tool execution, response processing, and agent switching. Each execution is
    independent and maintains its own isolated state.

    While Swarm includes basic orchestration features, its primary role is to serve
    as a reliable execution client for higher-level abstractions. It provides async
    streaming interfaces and supports 100+ language models through litellm.

    Key features:
        - Async streaming of responses and events
        - Tool execution and agent switching
        - Response validation and continuation
        - Automatic retries with backoff
        - Usage and cost tracking

    Examples:
        Basic usage:
            ```python
            from liteswarm import LLM, Agent, Message, Swarm, tool_plain


            @tool_plain
            def add(a: int, b: int) -> int:
                return a + b


            @tool_plain
            def multiply(a: int, b: int) -> int:
                return a * b


            # Create agent with tools
            agent = Agent(
                id="math",
                instructions="You are a math assistant.",
                llm=LLM(
                    model="gpt-4o",
                    parallel_tool_calls=False,
                ),
                tools=[add, multiply],
            )

            # Run agent execution
            swarm = Swarm()
            messages = [Message(role="user", content="Calculate 2 + 2")]
            result = await swarm.run(agent, messages=messages)

            print(result.final_response.content)  # "The result is 4"
            ```

        Stream events:
            ```python
            messages = [Message(role="user", content="Calculate (2 + 3) * 4")]
            stream = swarm.stream(agent, messages=messages)

            async for event in stream:
                if event.type == "agent_response_chunk":
                    print(event.chunk.completion.delta.content)
                elif event.type == "tool_call_result":
                    print(f"Tool result: {event.tool_call_result.return_value}")

            result = await stream.get_return_value()
            ```

        Agent switching:
            ```python
            from pydantic import BaseModel


            class ExpertParams(BaseModel):
                domain: str


            @tool_plain
            def switch_to_expert(domain: str) -> ToolResult:
                expert = Agent[ExpertParams, None](
                    id=f"{domain}-expert",
                    instructions=f"You are a {domain} expert.",
                    llm=LLM(model="gpt-4o"),
                    params_type=ExpertParams,
                )
                return ToolResult.switch_to(
                    content=f"Switching to {domain} expert",
                    agent=expert,
                    params=ExpertParams(domain=domain),
                )


            router = Agent(
                id="router",
                instructions="Route questions to experts.",
                llm=LLM(model="gpt-4o"),
                tools=[switch_to_expert],
            )

            messages = [Message(role="user", content="Explain quantum physics")]
            async for event in swarm.stream(router, messages=messages):
                if event.type == "agent_switch":
                    print(f"Switched to {event.current_agent.id}")
            ```

    Notes:
        - Each execution maintains isolated conversation state
        - Create separate instances for concurrent conversations
        - Safety limits prevent infinite loops and recursion
    """

    def __init__(
        self,
        max_retries: int = 3,
        initial_retry_delay: float = 1.0,
        max_retry_delay: float = 10.0,
        backoff_factor: float = 2.0,
        max_response_continuations: int = 5,
        max_agent_switches: int = 10,
        max_iterations: int = sys.maxsize,
        include_usage: bool = False,
        include_cost: bool = False,
        strict: bool = True,
    ) -> None:
        """Initialize a new Swarm instance.

        Creates a swarm instance with specified configuration for usage tracking,
        error recovery, and safety limits. Each execution maintains its own
        isolated conversation state.

        Args:
            max_retries: Maximum API retry attempts.
            initial_retry_delay: Initial retry delay in seconds.
            max_retry_delay: Maximum retry delay in seconds.
            backoff_factor: Multiplier for retry delay.
            max_response_continuations: Maximum response length continuations.
            max_agent_switches: Maximum allowed agent switches.
            max_iterations: Maximum processing iterations.
            include_usage: Whether to track token usage.
            include_cost: Whether to track response costs.
            strict: Whether to raise errors or handle them internally.

        Notes:
            - Each execution maintains isolated conversation state
            - Retry configuration uses exponential backoff
            - Safety limits prevent infinite loops and recursion
        """
        self._max_retries = max_retries
        self._initial_retry_delay = initial_retry_delay
        self._max_retry_delay = max_retry_delay
        self._backoff_factor = backoff_factor
        self._max_response_continuations = max_response_continuations
        self._max_agent_switches = max_agent_switches
        self._max_iterations = max_iterations
        self._include_usage = include_usage
        self._include_cost = include_cost
        self._strict = strict

    # ================================================
    # MARK: Tool Processing
    # ================================================

    def _parse_tool_call_result(
        self,
        tool_call: ChatCompletionDeltaToolCall,
        tool_return_value: Any,
    ) -> ToolCallResult:
        """Parse tool return value into framework result representation.

        Converts tool return values into ToolCallResult instances for internal processing.
        Handles two return types: ToolResult objects for type-safe tool execution results
        (with optional agent switches), and simple JSON-serializable values that become
        message content.

        Args:
            tool_call: Original tool call details.
            tool_return_value: Raw return value from tool function:
                - ToolResult for type-safe tool execution results
                - JSON-serializable value for simple responses

        Returns:
            ToolCallResult with processed result and context updates.

        Raises:
            SwarmError: If an Agent is returned directly.
        """

        def _create_tool_message(content: str) -> Message:
            return Message(
                role="tool",
                content=content,
                tool_call_id=tool_call.id,
            )

        log_verbose(
            f"Tool return value: {tool_return_value}",
            level="DEBUG",
        )

        match tool_return_value:
            case Agent():
                raise SwarmError("Use ToolResult.switch_to for switching between agents.")

            case ToolResult() as tool_result:
                content = parse_content(tool_result.content)
                return ToolCallResult(
                    tool_call=tool_call,
                    return_value=tool_return_value,
                    message=_create_tool_message(content),
                    agent_switch=tool_result.agent_switch,
                )

            case _:
                content = parse_content(tool_return_value)
                return ToolCallResult(
                    tool_call=tool_call,
                    return_value=tool_return_value,
                    message=_create_tool_message(content),
                )

    async def _process_tool_call(
        self,
        context: AgentContext,
        tool_call: ChatCompletionDeltaToolCall,
    ) -> ToolCallResult:
        """Process single tool call execution.

        Manages tool call lifecycle by validating tool existence, executing with context,
        handling errors, and processing results. Supports both regular return values
        and special cases like agent switching.

        Args:
            context: Agent context for execution.
            tool_call: Tool call details with function name and arguments.

        Returns:
            ToolCallResult containing execution result or error.

        Raises:
            SwarmError: If tool execution fails and strict mode is enabled.
        """
        tool_call_result: ToolCallResult
        tools = context.agent.tools
        function_name = tool_call.function.name
        function_tools_map = {tool.name: tool for tool in tools}

        if function_name not in function_tools_map:
            error = SwarmError(f"Unknown function: {function_name}")
            if self._strict:
                raise error

            return ToolCallResult(
                tool_call=tool_call,
                return_value=None,
                error=error,
                message=Message(
                    role="tool",
                    content=f"Unknown function: {function_name}",
                    tool_call_id=tool_call.id,
                ),
            )

        try:
            args = orjson.loads(tool_call.function.arguments)
            function_tool = function_tools_map[function_name]
            tool_return_value = await function_tool.run(context, **args)
            tool_call_result = self._parse_tool_call_result(
                tool_call=tool_call,
                tool_return_value=tool_return_value,
            )

        except Exception as e:
            error = SwarmError(f"Error executing tool: {e}", original_error=e)
            if self._strict:
                raise error from e

            tool_call_result = ToolCallResult(
                tool_call=tool_call,
                return_value=None,
                error=error,
                message=Message(
                    role="tool",
                    content=f"Error executing tool: {str(e)}",
                    tool_call_id=tool_call.id,
                ),
            )

        return tool_call_result

    async def _process_tool_calls(
        self,
        context: AgentContext,
        tool_calls: list[ChatCompletionDeltaToolCall],
    ) -> list[ToolCallResult]:
        """Process multiple tool calls with optimized execution.

        Handles tool calls using two strategies: direct execution for single calls
        to minimize overhead, and parallel execution with asyncio.gather for multiple
        calls. Preserves execution order in results.

        Args:
            context: Agent context for execution.
            tool_calls: List of tool calls to process.

        Returns:
            List of ToolCallResult objects in original call order.
        """
        tasks = [
            self._process_tool_call(
                context=context,
                tool_call=tool_call,
            )
            for tool_call in tool_calls
        ]

        results: list[ToolCallResult]
        match len(tasks):
            case 0:
                results = []
            case 1:
                results = [await tasks[0]]
            case _:
                results = await asyncio.gather(*tasks)

        return results

    # ================================================
    # MARK: Response Handling
    # ================================================

    def _prepare_completion_kwargs(
        self,
        context: AgentContext,
    ) -> dict[str, Any]:
        """Prepare completion kwargs for both sync and async completions.

        Configures message history, tool settings, response format, and usage tracking
        based on agent's configuration and context.

        Args:
            context: Agent context providing configuration and messages.

        Returns:
            Dictionary of completion kwargs ready for litellm.completion/acompletion.
        """
        exclude_keys = {"response_format", "litellm_kwargs"}
        llm_messages = dump_messages(context.messages, exclude_none=True)
        llm_kwargs = context.agent.llm.model_dump(exclude=exclude_keys, exclude_none=True)
        llm_override_kwargs = {
            "messages": llm_messages,
            "stream": True,
            "stream_options": {"include_usage": True} if self._include_usage else None,
            "tools": tools_to_json(context.agent.tools) if context.agent.tools else None,
        }

        response_format = context.agent.llm.response_format
        supported_params = litellm.get_supported_openai_params(context.agent.llm.model) or []
        if "response_format" in supported_params and response_format:
            llm_override_kwargs["response_format"] = response_format

            response_format_str: str | None = None
            if is_subtype(response_format, BaseModel):
                response_format_str = orjson.dumps(response_format.model_json_schema()).decode()
            else:
                response_format_str = orjson.dumps(response_format).decode()

            log_verbose(
                f"Using response format: {response_format_str}",
                level="DEBUG",
            )

        completion_kwargs = {
            **llm_kwargs,
            **llm_override_kwargs,
            **(context.agent.llm.litellm_kwargs or {}),
        }

        log_verbose(
            f"Sending messages to agent [{context.agent.id}]: {orjson.dumps(llm_messages).decode()}",
            level="DEBUG",
        )

        return completion_kwargs

    async def _create_completion(
        self,
        context: AgentContext,
    ) -> CustomStreamWrapper:
        """Create a completion request with agent's configuration.

        Prepares and sends a completion request using the agent's settings and
        message history, with proper error handling for context limits.

        Args:
            context: Agent context for completion.

        Returns:
            Response stream from the completion API.

        Raises:
            TypeError: If response format is unexpected.
            ContextWindowExceededError: If context window is exceeded.
        """
        completion_kwargs = self._prepare_completion_kwargs(context)
        response_stream = await litellm.acompletion(**completion_kwargs)
        if not isinstance(response_stream, CustomStreamWrapper):
            raise TypeError("Expected a CustomStreamWrapper instance.")

        return response_stream

    async def _continue_generation(
        self,
        context: AgentContext,
        previous_content: str,
    ) -> CustomStreamWrapper:
        """Continue generation after reaching output token limit.

        Creates a new completion request that continues from the previous content
        while maintaining the original context and settings.

        Args:
            context: Agent context for continuation.
            previous_content: Content generated before hitting limit.

        Returns:
            Response stream for the continuation request.
        """
        continuation_messages = [
            *context.messages,
            Message(role="assistant", content=previous_content),
            Message(role="user", content="Please continue your previous response."),
        ]

        return await self._create_completion(
            context=AgentContext(
                agent=context.agent,
                messages=continuation_messages,
                params=context.params,
            )
        )

    async def _get_completion_response(
        self,
        context: AgentContext,
    ) -> AsyncGenerator[CompletionResponseChunk, None]:
        """Stream completion response chunks from the language model.

        Manages the complete response lifecycle including continuation handling,
        error recovery, and usage tracking. Uses automatic retries with backoff
        for transient errors.

        Args:
            context: Agent context for completion.

        Yields:
            CompletionResponseChunk containing content updates and metadata.

        Raises:
            CompletionError: If completion fails after all retry attempts.
            ContextLengthError: If context exceeds limits and cannot be reduced.
        """
        try:
            accumulated_content: str = ""
            continuation_count: int = 0
            current_stream: CustomStreamWrapper = await self._get_initial_completion(
                context=context,
            )

            while continuation_count < self._max_response_continuations:
                async for chunk in current_stream:
                    response_chunk = self._process_completion_chunk(
                        agent=context.agent,
                        chunk=chunk,
                    )

                    yield response_chunk

                    if response_chunk.delta.content:
                        accumulated_content += response_chunk.delta.content

                    if response_chunk.finish_reason == "length":
                        continuation_count += 1
                        current_stream = await self._handle_response_continuation(
                            context=context,
                            continuation_count=continuation_count,
                            accumulated_content=accumulated_content,
                        )

                        # This break will exit the `for` loop, but the `while` loop
                        # will continue to process the response continuation
                        break
                else:
                    break

        except (CompletionError, ContextLengthError):
            raise

        except Exception as e:
            raise CompletionError(
                f"Failed to get completion response: {e}",
                original_error=e,
            ) from e

    async def _get_initial_completion(
        self,
        context: AgentContext,
    ) -> CustomStreamWrapper:
        """Create initial completion stream with error handling.

        Creates the first completion stream attempt with proper error handling
        for context length issues and token limits.

        Args:
            context: Agent context for completion.

        Returns:
            CustomStreamWrapper managing the completion response stream.

        Raises:
            CompletionError: If completion fails after exhausting retries.
            ContextLengthError: If context remains too large after reduction.
        """
        try:
            return await self._create_completion(context)
        except ContextWindowExceededError as e:
            model = context.agent.llm.model
            token_count = token_counter(model=model, messages=context.messages)
            max_tokens = context.agent.llm.max_tokens or get_max_tokens(model)
            err_message = f"Context window exceeded: {token_count}/{max_tokens} tokens for {model}"

            log_verbose(err_message, level="ERROR")

            raise ContextLengthError(
                message=err_message,
                model=model,
                current_length=token_count,
                max_length=max_tokens,
                original_error=e,
            ) from e

    def _process_completion_chunk(
        self,
        agent: Agent,
        chunk: ModelResponse,
    ) -> CompletionResponseChunk:
        """Process completion stream chunk into a structured response.

        Extracts response delta, finish reason, and calculates usage statistics
        from the raw chunk data.

        Args:
            agent: Agent providing model info and cost settings.
            chunk: Raw response chunk from the model API.

        Returns:
            Structured completion response with metadata.

        Raises:
            TypeError: If chunk format is invalid.
        """
        choice = chunk.choices[0]
        if not isinstance(choice, StreamingChoices):
            raise TypeError("Expected a StreamingChoices instance.")

        delta = Delta.from_delta(choice.delta)
        finish_reason = choice.finish_reason
        usage: Usage | None = safe_get_attr(chunk, "usage", Usage)
        response_cost: ResponseCost | None = None

        if usage is not None and self._include_cost:
            response_cost = calculate_response_cost(
                model=agent.llm.model,
                usage=usage,
            )

        return CompletionResponseChunk(
            id=chunk.id,
            delta=delta,
            finish_reason=finish_reason,
            usage=usage,
            response_cost=response_cost,
        )

    async def _handle_response_continuation(
        self,
        context: AgentContext,
        continuation_count: int,
        accumulated_content: str,
    ) -> CustomStreamWrapper:
        """Handle response continuation with proper limits.

        Creates a new completion stream that continues the previous response
        while enforcing maximum continuation limits.

        Args:
            context: Agent context for continuation.
            continuation_count: Number of continuations performed.
            accumulated_content: Previously generated content.

        Returns:
            New stream for continuation.

        Raises:
            MaxResponseContinuationsError: If maximum continuations reached.
        """
        if continuation_count >= self._max_response_continuations:
            generated_tokens = token_counter(
                model=context.agent.llm.model,
                text=accumulated_content,
            )

            raise MaxResponseContinuationsError(
                message=f"Maximum response continuations ({self._max_response_continuations}) reached",
                continuation_count=continuation_count,
                max_continuations=self._max_response_continuations,
                total_tokens=generated_tokens,
            )

        log_verbose(
            f"Response continuation {continuation_count}/{self._max_response_continuations}",
            level="INFO",
        )

        return await self._continue_generation(
            context=context,
            previous_content=accumulated_content,
        )

    def _should_parse_agent_response(
        self,
        model: str,
        custom_llm_provider: str | None = None,
        response_format: ResponseFormat | None = None,
    ) -> bool:
        """Determine if response content requires parsing.

        Checks if the model supports structured output and if a response format
        is specified. Only enables parsing when both conditions are met.

        Args:
            model: Model identifier to check for format support.
            custom_llm_provider: Optional custom provider to check.
            response_format: Format specification to evaluate.

        Returns:
            True if content should be parsed based on format and model capabilities.
        """
        if not response_format:
            return False

        if is_subtype(response_format, BaseModel) or is_subtype(response_format, ResponseSchema):
            return litellm.supports_response_schema(model, custom_llm_provider)

        if is_subtype(response_format, ResponseFormatJsonSchema):
            return True

        return False

    @returnable
    async def _stream_agent_response(
        self,
        context: AgentContext,
    ) -> AsyncStream[SwarmEvent, AgentResponse]:
        """Stream agent response and process completion events.

        Streams raw completion chunks and agent response chunks from the language model.
        Accumulates content and tool calls incrementally, with optional response parsing
        based on the agent response format configuration.

        Args:
            context: Agent context for response generation.

        Returns:
            ReturnableAsyncGenerator yielding completion and response events,
            returning the final accumulated agent response.

        Raises:
            CompletionError: If completion fails after retries.
            ContextLengthError: If context exceeds limits after reduction.
        """
        snapshot_content: str | None = None
        snapshot_tool_calls: list[ChatCompletionDeltaToolCall] = []
        should_parse_chunks = self._should_parse_agent_response(
            model=context.agent.llm.model,
            response_format=context.agent.llm.response_format,
        )

        create_completion_stream = retry_wrapper(
            self._get_completion_response,
            max_retries=self._max_retries,
            initial_delay=self._initial_retry_delay,
            max_delay=self._max_retry_delay,
            backoff_factor=self._backoff_factor,
        )

        completion_stream = create_completion_stream(context)
        async for completion_chunk in completion_stream:
            yield YieldItem(CompletionResponseChunkEvent(chunk=completion_chunk))

            delta = completion_chunk.delta
            if delta.content:
                if snapshot_content is None:
                    snapshot_content = delta.content
                else:
                    snapshot_content += delta.content

            chunk_parsed: JSON | None = None
            if should_parse_chunks and snapshot_content:
                chunk_parsed = parse_partial_response(snapshot_content, strict=self._strict)

            if delta.tool_calls:
                for tool_call in delta.tool_calls:
                    if tool_call.id:
                        snapshot_tool_calls.append(tool_call)
                    elif snapshot_tool_calls:
                        last_tool_call = snapshot_tool_calls[-1]
                        last_tool_call.function.arguments += tool_call.function.arguments

            response_chunk = AgentResponseChunk(
                completion=completion_chunk,
                snapshot=snapshot_content,
                parsed=chunk_parsed,
                tool_calls=snapshot_tool_calls,
            )

            yield YieldItem(
                AgentResponseChunkEvent(
                    agent=context.agent,
                    chunk=response_chunk,
                )
            )

        output: Any = None
        if snapshot_content:
            output = parse_agent_output(
                content=snapshot_content,
                context=context,
                strict=self._strict,
            )

        agent_response = AgentResponse(
            id=completion_chunk.id,
            role=completion_chunk.delta.role,
            finish_reason=completion_chunk.finish_reason,
            content=snapshot_content,
            output=output,
            tool_calls=snapshot_tool_calls,
            usage=completion_chunk.usage,
            response_cost=completion_chunk.response_cost,
        )

        yield ReturnItem(agent_response)

    @returnable
    async def _process_agent_response(
        self,
        context: AgentContext,
        content: str | None,
        tool_calls: list[ChatCompletionDeltaToolCall] | None = None,
    ) -> AsyncStream[SwarmEvent, AgentResponseResult]:
        """Process agent response content and execute tool calls.

        Creates assistant message from response content and processes any tool calls
        sequentially. Tool results can trigger agent switches through ToolResult.switch_to.
        All messages (assistant, tool results) are collected for conversation history.

        Args:
            context: Agent context for processing.
            content: Text content from agent response.
            tool_calls: Tool calls to execute in sequence.

        Returns:
            ReturnableAsyncGenerator yielding events and returning agent response processing results.

        Raises:
            SwarmError: If tool execution fails and strict mode is enabled.
        """
        new_messages: list[Message] = []
        agent_switches: list[AgentSwitch] = []

        tool_calls = tool_calls or None
        response_message = Message(role="assistant", content=content, tool_calls=tool_calls)
        new_messages.append(response_message)

        if tool_calls:
            tool_call_results = await self._process_tool_calls(
                context=context,
                tool_calls=tool_calls,
            )

            for tool_call_result in tool_call_results:
                yield YieldItem(
                    ToolCallResultEvent(
                        agent=context.agent,
                        tool_call_result=tool_call_result,
                    )
                )

                agent_switch = tool_call_result.agent_switch
                if agent_switch is not None:
                    context.agent.invalidate()
                    agent_switches.append(agent_switch)

                new_messages.append(tool_call_result.message)

        yield ReturnItem(
            AgentResponseResult(
                new_messages=new_messages,
                agent_switches=agent_switches,
            )
        )

    # ================================================
    # MARK: Agent Management
    # ================================================

    def _create_agent_context(
        self,
        context: AgentContext,
        instructions: str | None = None,
    ) -> AgentContext:
        """Create agent context with properly ordered messages.

        Constructs a new agent context with a system message containing instructions
        followed by the filtered conversation history. Instructions are either provided
        directly or resolved from the agent's template.

        Args:
            context: Current agent context providing base state.
            instructions: Optional pre-resolved instructions.

        Returns:
            New agent context with ordered messages and resolved instructions.
        """
        if instructions is None:
            instructions = resolve_agent_instructions(context)

        system_message = Message(role="system", content=instructions)
        agent_messages = [message for message in context.messages if message.role != "system"]
        messages = [system_message, *agent_messages]

        return AgentContext(
            agent=context.agent,
            messages=messages,
            params=context.params,
        )

    @returnable
    async def _stream_agent_iteration(
        self,
        context: AgentContext,
    ) -> AsyncStream[SwarmEvent, AgentIterationResult]:
        """Stream events for a single agent processing iteration.

        Manages one complete iteration of agent processing including instruction resolution,
        response generation, tool calls, and message collection. The iteration continues
        until the agent becomes stale or completes its task.

        Args:
            context: Current agent context for this iteration.

        Returns:
            ReturnableAsyncGenerator yielding events and returning iteration results.
        """
        new_messages: list[Message] = []
        agent_switches: list[AgentSwitch] = []
        instructions = resolve_agent_instructions(context)
        iteration_context = self._create_agent_context(
            context=context,
            instructions=instructions,
        )

        yield YieldItem(AgentStartEvent(context=iteration_context, instructions=instructions))

        response_stream = self._stream_agent_response(iteration_context)
        async for event in response_stream:
            yield YieldItem(event)

        response = await response_stream.get_return_value()
        yield YieldItem(AgentResponseEvent(agent=iteration_context.agent, response=response))

        if response.content or response.tool_calls:
            response_result_stream = self._process_agent_response(
                context=iteration_context,
                content=response.content,
                tool_calls=response.tool_calls,
            )

            async for event in response_result_stream:
                yield YieldItem(event)

            response_result = await response_result_stream.get_return_value()
            new_messages.extend(response_result.new_messages)
            agent_switches.extend(response_result.agent_switches)
        else:
            # We might not want to do this, but it's a good fallback
            # Please consider removing this if it leads to unexpected behavior
            new_messages.append(Message(role="assistant", content="<empty>"))
            log_verbose(
                "Empty response received, appending placeholder message",
                level="WARNING",
            )

        # If agent response contains tool calls, we do not invalidate the agent
        # because most llms will expect an assistant response after a tool message
        if not response.tool_calls:
            iteration_context.agent.invalidate()
            log_verbose(
                f"No tool calls found, invalidating agent {iteration_context.agent.id}",
                level="DEBUG",
            )

        yield YieldItem(
            AgentCompleteEvent(
                context=iteration_context,
                instructions=instructions,
                response=response,
                new_messages=new_messages,
            )
        )

        yield ReturnItem(
            AgentIterationResult(
                context=iteration_context,
                agent_response=response,
                new_messages=new_messages,
                agent_switches=agent_switches,
            )
        )

    @returnable
    async def _stream_agent_run(
        self,
        context: AgentContext,
        iteration_count: int,
        switch_count: int,
        switch_history: list[str],
    ) -> AsyncStream[SwarmEvent, AgentRunResult]:
        """Stream events from active agent and manage agent switching.

        Core execution loop that processes agent responses, handles tool calls,
        and manages agent switches. Continues execution until no active agents
        remain or safety limits are reached.

        Args:
            context: Initial agent context.
            iteration_count: Current number of processing iterations.
            switch_count: Number of agent switches performed.
            switch_history: List of agent IDs that have been switched.

        Returns:
            ReturnableAsyncGenerator yielding events and returning complete run results.

        Raises:
            MaxAgentSwitchesError: If too many agent switches occur.
            SwarmError: If no agent response is received.
        """
        current_context = context
        current_agent = context.agent
        current_messages = [*context.messages]
        current_params = context.params

        agent_responses: list[AgentResponse] = []
        agent_switch_queue: deque[AgentSwitch] = deque()
        all_messages: list[Message] = [*current_messages]
        new_messages: list[Message] = []

        while iteration_count < self._max_iterations:
            iteration_count += 1
            if current_agent.is_stale:
                if switch_count >= self._max_agent_switches:
                    raise MaxAgentSwitchesError(
                        message=f"Maximum number of agent switches ({self._max_agent_switches}) exceeded",
                        switch_count=switch_count,
                        max_switches=self._max_agent_switches,
                        switch_history=switch_history,
                    )

                if not agent_switch_queue:
                    log_verbose(
                        "No more pending agents, stopping execution",
                        level="DEBUG",
                    )
                    break

                agent_switch = agent_switch_queue.popleft()

                previous_agent = current_agent
                current_agent = agent_switch.agent
                current_params = agent_switch.params
                if agent_switch.messages is not None:
                    current_messages = agent_switch.messages

                switch_count += 1
                switch_history.append(current_agent.id)
                current_agent.activate()

                log_verbose(
                    f"Switching from agent {previous_agent.id} to {current_agent.id}",
                    level="DEBUG",
                )

                yield YieldItem(
                    AgentSwitchEvent(
                        previous_agent=previous_agent,
                        current_agent=current_agent,
                    )
                )

            current_context = AgentContext(
                agent=current_agent,
                messages=current_messages,
                params=current_params,
            )

            iteration_stream = self._stream_agent_iteration(current_context)
            async for event in iteration_stream:
                yield YieldItem(event)

            iteration_result = await iteration_stream.get_return_value()

            agent_responses.append(iteration_result.agent_response)

            current_messages.extend(iteration_result.new_messages)
            all_messages.extend(iteration_result.new_messages)
            new_messages.extend(iteration_result.new_messages)

            agent_switch_queue.extend(iteration_result.agent_switches)

        if not agent_responses:
            raise SwarmError("No agent response received")

        result = AgentRunResult(
            id=str(uuid.uuid4()),
            final_context=current_context,
            final_response=agent_responses[-1],
            agent_responses=agent_responses,
            new_messages=new_messages,
            all_messages=all_messages,
        )

        yield ReturnItem(result)

    @returnable
    async def _create_event_stream(
        self,
        context: AgentContext,
    ) -> AsyncStream[SwarmEvent, AgentRunResult]:
        """Create the base event stream for swarm execution.

        Initializes and manages the complete execution lifecycle including agent
        activation, message processing, and result collection. This is the core
        implementation of swarm's event streaming capabilities.

        Args:
            context: Initial agent context for execution.

        Returns:
            ReturnableAsyncGenerator yielding events and returning execution results.

        Raises:
            SwarmError: If messages list is empty.
            ContextLengthError: If context becomes too large.
            MaxAgentSwitchesError: If too many switches occur.
            MaxResponseContinuationsError: If response needs too many continuations.
        """
        if not context.messages:
            raise SwarmError("Messages list is empty")

        current_agent = context.agent
        current_agent.activate()

        yield YieldItem(AgentRunStartEvent(context=context))

        agent_execution_stream = self._stream_agent_run(
            context=context,
            iteration_count=0,
            switch_count=0,
            switch_history=[],
        )

        async for event in agent_execution_stream:
            yield YieldItem(event)

        result = await agent_execution_stream.get_return_value()
        yield YieldItem(AgentRunCompleteEvent(run_result=result))
        yield ReturnItem(result)

    # ================================================
    # MARK: Public Interface
    # ================================================

    def stream(
        self,
        agent: Agent[ContextParams, AgentOutput],
        messages: list[Message],
        params: ContextParams = _None,
        final_params_type: type[FinalContextParams] | None = None,
        final_output_type: type[FinalOutputType] | None = None,
    ) -> SwarmStream[FinalContextParams, FinalOutputType]:
        """Start agent execution and stream events with type validation.

        Main entry point for swarm execution. Streams events in real-time during
        execution and validates final types. Supports both event processing and
        final result collection.

        Args:
            agent: Agent that will process the messages.
            messages: List of conversation messages.
            params: Context parameters matching agent's params_type.
            final_params_type: Optional type to validate final parameters against.
            final_output_type: Optional type to validate final output against.

        Returns:
            SwarmStream yielding events and returning validated result.

        Raises:
            SwarmError: If execution fails or type validation fails.
            ContextLengthError: If context exceeds model limits.
            MaxAgentSwitchesError: If too many agent switches occur.
            MaxResponseContinuationsError: If response needs too many continuations.

        Example:
            ```python
            from pydantic import BaseModel


            class MathParams(BaseModel):
                precision: int


            class MathResult(BaseModel):
                result: int
                explanation: str


            agent = Agent[MathParams, MathResult](
                id="math",
                instructions="You are a math assistant.",
                llm=LLM(
                    model="gpt-4o",
                    response_format=MathResult,
                ),
                params_type=MathParams,
                result_type=MathResult,
            )

            messages = [Message(role="user", content="Calculate 2 + 2")]
            stream = swarm.stream(
                agent=agent,
                messages=messages,
                params=MathParams(precision=2),
                final_output_type=MathResult,
            )

            async for event in stream:
                if event.type == "agent_response_chunk":
                    print(event.chunk.completion.delta.content)

            result = await stream.get_return_value()
            print(result.final_response.output.result)  # Type-safe access
            ```

        Notes:
            - Events are streamed in real-time during execution
            - Type validation ensures safe access to results
            - Context parameters must match agent's params_type
        """
        context = AgentContext(
            agent=agent,
            messages=messages,
            params=params,
        )

        event_stream = self._create_event_stream(context)

        return SwarmStream(
            event_stream,
            final_params_type=final_params_type,
            final_output_type=final_output_type,
            strict=self._strict,
        )

    async def run(
        self,
        agent: Agent[ContextParams, AgentOutput],
        messages: list[Message],
        params: ContextParams = _None,
        final_params_type: type[FinalContextParams] | None = None,
        final_output_type: type[FinalOutputType] | None = None,
    ) -> AgentRunResult[FinalContextParams, FinalOutputType]:
        """Execute agent and return final result with type validation.

        Convenience method that wraps stream() for direct result collection.
        Executes the agent with provided messages and validates final types
        without requiring event handling.

        Args:
            agent: Agent that will process the messages.
            messages: List of conversation messages.
            params: Context parameters matching agent's params_type.
            final_params_type: Optional type to validate final parameters against.
            final_output_type: Optional type to validate final output against.

        Returns:
            Complete execution result with validated types.

        Raises:
            SwarmError: If execution fails or type validation fails.
            ContextLengthError: If context exceeds model limits.
            MaxAgentSwitchesError: If too many agent switches occur.
            MaxResponseContinuationsError: If response needs too many continuations.

        Example:
            ```python
            from pydantic import BaseModel


            class MathParams(BaseModel):
                precision: int


            class MathResult(BaseModel):
                result: int
                explanation: str


            agent = Agent[MathParams, MathResult](
                id="math",
                instructions="You are a math assistant.",
                llm=LLM(
                    model="gpt-4o",
                    response_format=MathResult,
                ),
                params_type=MathParams,
                result_type=MathResult,
            )

            messages = [Message(role="user", content="Calculate 2 + 2")]
            result = await swarm.run(
                agent=agent,
                messages=messages,
                params=MathParams(precision=2),
                final_output_type=MathResult,
            )
            print(result.final_response.output.result)  # Type-safe access
            ```

        Notes:
            - Simplified interface for getting validated result
            - Internally uses stream() but handles events
            - Context parameters must match agent's params_type
        """
        stream = self.stream(
            agent=agent,
            messages=messages,
            params=params,
            final_params_type=final_params_type,
            final_output_type=final_output_type,
        )

        return await stream.get_return_value()
