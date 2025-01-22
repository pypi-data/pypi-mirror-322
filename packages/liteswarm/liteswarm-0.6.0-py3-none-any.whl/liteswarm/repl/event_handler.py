# Copyright 2025 GlyphyAI
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import sys
from typing import TYPE_CHECKING

from liteswarm.types.events import (
    AgentCompleteEvent,
    AgentResponseChunkEvent,
    AgentRunCompleteEvent,
    AgentRunStartEvent,
    AgentSwitchEvent,
    ErrorEvent,
    SwarmEvent,
    ToolCallResultEvent,
)

if TYPE_CHECKING:
    from liteswarm.types.agent import Agent


class ConsoleEventHandler:
    """Console event handler providing formatted output for REPL interactions.

    Processes and displays Swarm events with distinct visual indicators for
    different event types. Maintains message continuity and provides clear
    feedback for each event type.

    Examples:
        Handling events from the agent execution stream:
            ```python
            handler = ConsoleEventHandler()

            async for event in swarm.execute(agent, messages):
                handler.on_event(event)
            ```

    Note:
        This is an internal event handler and is not intended to be used by
        end-users. You should handle events on your own when receiving them
        from the agent execution stream.
    """

    def __init__(self) -> None:
        """Initialize event handler with message continuity tracking."""
        super().__init__()
        self._last_agent: Agent | None = None

    def on_event(self, event: SwarmEvent) -> None:
        """Process and display a Swarm event with appropriate formatting."""
        match event:
            # Agent Events
            case AgentRunStartEvent():
                self._handle_agent_execution_start(event)
            case AgentResponseChunkEvent():
                self._handle_response_chunk(event)
            case ToolCallResultEvent():
                self._handle_tool_call_result(event)
            case AgentSwitchEvent():
                self._handle_agent_switch(event)
            case AgentCompleteEvent():
                self._handle_agent_complete(event)
            case AgentRunCompleteEvent():
                self._handle_agent_execution_complete(event)

            # System Events
            case ErrorEvent():
                self._handle_error(event)

    # ================================================
    # MARK: Agent Events
    # ================================================

    def _handle_agent_execution_start(self, event: AgentRunStartEvent) -> None:
        """Display agent execution start message."""
        agent_id = event.context.agent.id
        print(f"\n\n🔧 [{agent_id}] Agent execution started\n", flush=True)

    def _handle_response_chunk(self, event: AgentResponseChunkEvent) -> None:
        """Display streaming response chunk with agent context."""
        completion = event.chunk.completion
        if completion.finish_reason == "length":
            print("\n[...continuing...]", end="", flush=True)

        if content := completion.delta.content:
            if self._last_agent != event.agent:
                agent_id = event.agent.id
                print(f"\n[{agent_id}] ", end="", flush=True)
                self._last_agent = event.agent

            print(content, end="", flush=True)

        if completion.finish_reason:
            print("", flush=True)

    def _handle_tool_call_result(self, event: ToolCallResultEvent) -> None:
        """Display tool call result with function details."""
        agent_id = event.agent.id
        tool_call = event.tool_call_result.tool_call
        tool_name = tool_call.function.name
        tool_id = tool_call.id
        print(f"\n📎 [{agent_id}] Tool '{tool_name}' [{tool_id}] called")

    def _handle_agent_switch(self, event: AgentSwitchEvent) -> None:
        """Display agent switch notification."""
        prev_id = event.previous_agent.id
        curr_id = event.current_agent.id
        print(f"\n🔄 Switched from {prev_id} to {curr_id}...")

    def _handle_agent_complete(self, event: AgentCompleteEvent) -> None:
        """Display agent completion status."""
        agent_id = event.context.agent.id
        print(f"\n✅ [{agent_id}] Completed", flush=True)
        self._last_agent = None

    def _handle_agent_execution_complete(self, event: AgentRunCompleteEvent) -> None:
        """Display execution completion status."""
        self._last_agent_id = None
        print("\n\n✅ Completed\n", flush=True)

    # ================================================
    # MARK: System Events
    # ================================================

    def _handle_error(self, event: ErrorEvent) -> None:
        """Display error message with agent context."""
        agent_id = event.agent.id if event.agent else "unknown"
        print(f"\n❌ [{agent_id}] Error: {str(event.error)}", file=sys.stderr)
        self._last_agent = None
