# Copyright 2025 GlyphyAI
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from typing import Any, Generic

from pydantic import ConfigDict, field_serializer

from liteswarm.types.agent import AgentContext, AgentOutput, ContextParams
from liteswarm.types.base import SwarmBaseModel
from liteswarm.types.llm import Delta, FinishReason, Message, MessageRole, ResponseCost, ToolCall, Usage
from liteswarm.types.tools import AgentSwitch
from liteswarm.types.typing import JSON


class ToolCallResult(SwarmBaseModel, Generic[ContextParams, AgentOutput]):
    """Complete result of a tool execution.

    Contains original call, return value, response message, and any
    state updates or errors that occurred during execution.
    """

    tool_call: ToolCall
    """Original tool call from the agent."""

    return_value: Any
    """Raw value returned by the tool."""

    message: Message
    """Response message for conversation history."""

    agent_switch: AgentSwitch[ContextParams, AgentOutput] | None = None
    """Optional request to switch to another agent."""

    error: Exception | None = None
    """Error that occurred during execution, if any."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_attribute_docstrings=True,
        extra="forbid",
    )

    @field_serializer("return_value")
    def serialize_tool_return_value(self, value: Any) -> str:
        """Serialize tool return value."""
        return str(value) if value else "None"

    @field_serializer("error")
    def serialize_tool_error(self, error: Exception | None) -> str:
        """Serialize tool error."""
        return str(error) if error else "None"


class CompletionResponseChunk(SwarmBaseModel):
    """Raw chunk from model completion stream.

    Contains incremental content updates and optional usage tracking
    in the final chunk when enabled.
    """

    id: str
    """Unique identifier for the completion."""

    delta: Delta
    """Incremental content and tool updates."""

    finish_reason: FinishReason | None = None
    """Why the response generation stopped."""

    usage: Usage | None = None
    """Token usage statistics if tracking enabled."""

    response_cost: ResponseCost | None = None
    """Cost calculation if tracking enabled."""


class AgentResponseChunk(SwarmBaseModel):
    """Processed chunk of agent response stream.

    Contains both raw completion data and accumulated content from
    previous chunks. Maintains running state of content, tool calls,
    and any parsed structured output.
    """

    completion: CompletionResponseChunk
    """Raw chunk from model."""

    snapshot: str | None = None
    """Accumulated response content."""

    parsed: JSON | None = None
    """Partially parsed structured output."""

    tool_calls: list[ToolCall] | None = None
    """Accumulated tool calls."""


class AgentResponse(SwarmBaseModel, Generic[AgentOutput]):
    """Complete response from an agent execution.

    Final state after all chunks are processed, including content,
    tool calls, and execution statistics.
    """

    id: str
    """Unique identifier for the response."""

    role: MessageRole | None = None
    """Role in conversation history."""

    finish_reason: FinishReason | None = None
    """Reason for response generation stopping."""

    content: str | None = None
    """Final response content."""

    output: AgentOutput | None = None
    """Parsed structured output if specified."""

    tool_calls: list[ToolCall] | None = None
    """All tool calls made during execution."""

    usage: Usage | None = None
    """Token usage if tracking enabled."""

    response_cost: ResponseCost | None = None
    """Cost calculation if tracking enabled."""


class AgentResponseResult(SwarmBaseModel):
    """Result of processing an agent response.

    Contains new messages and agent switches that occurred
    during response processing.
    """

    new_messages: list[Message]
    """New messages generated."""

    agent_switches: list[AgentSwitch]
    """Agent switches requested during response processing."""


class AgentIterationResult(SwarmBaseModel, Generic[ContextParams, AgentOutput]):
    """Result of a single agent iteration.

    Contains the final state after one complete iteration, including
    response, messages, and agent switches.
    """

    context: AgentContext[ContextParams, AgentOutput]
    """Agent context after iteration."""

    agent_response: AgentResponse[AgentOutput]
    """Final response from this iteration."""

    new_messages: list[Message]
    """Messages generated in this iteration."""

    agent_switches: list[AgentSwitch]
    """Agent switches requested in this iteration."""


class AgentRunResult(SwarmBaseModel, Generic[ContextParams, AgentOutput]):
    """Complete result of an agent execution.

    Contains the final state after all iterations, including full
    execution history and conversation state.
    """

    id: str
    """Unique identifier for the run."""

    final_context: AgentContext[ContextParams, AgentOutput]
    """Last agent context."""

    final_response: AgentResponse[AgentOutput]
    """Last agent response in execution."""

    agent_responses: list[AgentResponse]
    """All agent responses from execution."""

    new_messages: list[Message]
    """Messages generated during execution."""

    all_messages: list[Message]
    """Complete conversation history."""
