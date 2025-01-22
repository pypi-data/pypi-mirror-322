# Copyright 2025 GlyphyAI
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from typing import Annotated, Generic, Literal

from pydantic import Discriminator, field_serializer

from liteswarm.types.agent import Agent, AgentContext, AgentOutput, ContextParams
from liteswarm.types.llm import Message
from liteswarm.types.swarm import (
    AgentResponse,
    AgentResponseChunk,
    AgentRunResult,
    CompletionResponseChunk,
    SwarmBaseModel,
    ToolCallResult,
)


class SwarmEventBase(SwarmBaseModel):
    """Base class for all Swarm events in the system.

    Used for pattern matching and routing of events throughout the system.
    All event types inherit from this class and implement specific event data.
    """

    type: str
    """Event type identifier."""


class AgentRunStartEvent(SwarmEventBase, Generic[ContextParams, AgentOutput]):
    """Event emitted when agent execution starts.

    Called at the very beginning of agent execution flow, before any
    message processing or tool calls. Used to initialize execution
    state and prepare for incoming events.
    """

    type: Literal["agent_run_start"] = "agent_run_start"
    """Event type identifier."""

    context: AgentContext[ContextParams, AgentOutput]
    """Initial agent context."""


class AgentRunCompleteEvent(SwarmEventBase, Generic[ContextParams, AgentOutput]):
    """Event emitted when agent execution completes.

    Called when an agent execution flow reaches completion, after all
    message processing and tool calls are done. Contains the final
    execution result with all responses and messages.
    """

    type: Literal["agent_run_complete"] = "agent_run_complete"
    """Event type identifier."""

    run_result: AgentRunResult[ContextParams, AgentOutput]
    """Complete run result."""


class CompletionResponseChunkEvent(SwarmEventBase):
    """Event emitted for each streaming update from the language model.

    Called each time new content is received from the model, before any
    agent-specific processing occurs. Used for monitoring raw model output.
    """

    type: Literal["completion_response_chunk"] = "completion_response_chunk"
    """Event type identifier."""

    chunk: CompletionResponseChunk
    """Raw completion response chunk."""


class AgentResponseChunkEvent(SwarmEventBase, Generic[ContextParams, AgentOutput]):
    """Event emitted for each streaming update from an agent.

    Called each time new content is received from an agent, including both
    text content and tool call updates. Used for real-time monitoring of
    agent responses.
    """

    type: Literal["agent_response_chunk"] = "agent_response_chunk"
    """Event type identifier."""

    agent: Agent[ContextParams, AgentOutput]
    """Agent that generated the response chunk."""

    chunk: AgentResponseChunk
    """Processed response chunk."""


class AgentResponseEvent(SwarmEventBase, Generic[ContextParams, AgentOutput]):
    """Event emitted when agent generates a complete response.

    Called after all response content and tool calls are processed, but before
    any state transitions occur. Used to capture the full agent response
    before it affects system state.
    """

    type: Literal["agent_response"] = "agent_response"
    """Event type identifier."""

    agent: Agent[ContextParams, AgentOutput]
    """Agent that generated response."""

    response: AgentResponse[AgentOutput]
    """Complete agent response."""


class ToolCallResultEvent(SwarmEventBase, Generic[ContextParams, AgentOutput]):
    """Event emitted when a tool call execution completes.

    Called after a tool finishes execution, with either a result or error.
    Used for processing tool outputs and updating system state.
    """

    type: Literal["tool_call_result"] = "tool_call_result"
    """Event type identifier."""

    agent: Agent[ContextParams, AgentOutput]
    """Agent that called the tool."""

    tool_call_result: ToolCallResult[ContextParams, AgentOutput]
    """Tool execution result."""


class AgentStartEvent(SwarmEventBase, Generic[ContextParams, AgentOutput]):
    """Event emitted when an agent iteration starts.

    Called at the beginning of an agent iteration, before any message
    processing or tool calls begin. Contains the prepared context and
    resolved instructions for this processing pass.
    """

    type: Literal["agent_start"] = "agent_start"
    """Event type identifier."""

    context: AgentContext[ContextParams, AgentOutput]
    """Initial context for this iteration."""

    instructions: str
    """Resolved agent instructions."""


class AgentCompleteEvent(SwarmEventBase, Generic[ContextParams, AgentOutput]):
    """Event emitted when an agent iteration completes.

    Called at the end of an agent iteration, after all responses and
    tool calls are processed. The same agent may execute again if it
    has not become stale after this iteration.
    """

    type: Literal["agent_complete"] = "agent_complete"
    """Event type identifier."""

    context: AgentContext[ContextParams, AgentOutput]
    """Final context after processing all messages and tool calls."""

    instructions: str
    """Resolved agent instructions."""

    response: AgentResponse[AgentOutput]
    """Final response accumulated during this iteration."""

    new_messages: list[Message]
    """Messages generated during this iteration."""


class AgentSwitchEvent(SwarmEventBase):
    """Event emitted when switching between agents.

    Called when the conversation switches from one agent to another.
    Both previous and current agents are always present.
    """

    type: Literal["agent_switch"] = "agent_switch"
    """Event type identifier."""

    previous_agent: Agent
    """Agent being switched from."""

    current_agent: Agent
    """Agent being switched to."""


class ErrorEvent(SwarmEventBase, Generic[ContextParams, AgentOutput]):
    """Event emitted when an error occurs during execution.

    Called when an error occurs during any phase of operation, including
    content generation, tool calls, or response processing. The agent
    may be None if the error occurred outside agent context.
    """

    type: Literal["error"] = "error"
    """Event type identifier."""

    agent: Agent[ContextParams, AgentOutput] | None
    """Agent that encountered the error, None for system-level errors."""

    error: Exception
    """Error that occurred."""

    @field_serializer("error")
    def serialize_error(self, error: Exception) -> str:
        """Serialize Exception object to string representation.

        This method is used by Pydantic to convert Exception objects into
        a serializable format for JSON encoding. It ensures that error
        information can be properly transmitted and logged.

        Args:
            error: Exception object to serialize.

        Returns:
            String representation of the error.
        """
        return str(error)


SwarmEvent = Annotated[
    AgentRunStartEvent
    | AgentRunCompleteEvent
    | CompletionResponseChunkEvent
    | AgentResponseChunkEvent
    | AgentResponseEvent
    | ToolCallResultEvent
    | AgentStartEvent
    | AgentCompleteEvent
    | AgentSwitchEvent
    | ErrorEvent,
    Discriminator("type"),
]
"""Type alias for all Swarm events."""
