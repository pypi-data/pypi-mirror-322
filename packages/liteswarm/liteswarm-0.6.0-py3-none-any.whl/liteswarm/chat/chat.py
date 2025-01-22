# Copyright 2025 GlyphyAI
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from typing import Any, Protocol, TypeVar

from typing_extensions import override

from liteswarm.chat.context import ChatContext, SwarmChatContext
from liteswarm.core.swarm import FinalContextParams, FinalOutputType, Swarm
from liteswarm.types.agent import Agent, AgentOutput, ContextParams
from liteswarm.types.chat import ChatMessage, ChatResponse, OptimizationStrategy
from liteswarm.types.collections import AsyncStream, ReturnableAsyncGenerator, ReturnItem, YieldItem, returnable
from liteswarm.types.events import SwarmEvent
from liteswarm.types.llm import Message
from liteswarm.types.typing import _None
from liteswarm.utils.misc import resolve_agent_instructions

ReturnType = TypeVar("ReturnType")
"""Type variable for chat return type."""


class Chat(Protocol[ReturnType]):
    """Protocol for stateful conversations using Swarm runtime.

    Provides a standard interface for maintaining conversation state
    while using Swarm for agent execution. Implementations can use
    different storage backends while maintaining consistent state access.

    Type Parameters:
        ReturnType: Type returned by message sending operations.

    Examples:
        ```python
        class MyChat(Chat[ChatResponse]):
            async def send_message(
                self,
                message: str,
                *,
                agent: Agent,
                context_variables: ContextVariables | None = None,
            ) -> ReturnableAsyncGenerator[SwarmEvent, ChatResponse]:
                # Process message and generate response
                async for event in self._process_message(message, agent):
                    yield YieldItem(event)
                yield ReturnItem(ChatResponse(...))


        # Use custom chat implementation
        chat = MyChat()

        # Initialize with existing history
        await chat.set_messages(
            [
                Message(role="system", content="You are a helpful assistant."),
                Message(role="user", content="What's the weather?"),
                Message(role="assistant", content="It's sunny!"),
            ]
        )

        async for event in chat.send_message(
            "Hello!",
            agent=my_agent,
            context_variables={"user": "Alice"},
        ):
            print(event)
        ```

    Notes:
        - Each chat maintains isolated conversation state
        - All operations are asynchronous by framework design
        - Message order must be preserved
        - Context optimization uses type-safe strategies
    """

    def send_message(
        self,
        message: str,
        *args: Any,
        **kwargs: Any,
    ) -> ReturnableAsyncGenerator[SwarmEvent, ReturnType]:
        """Send message and get response with conversation history.

        Processes the message using the specified agent, applying context
        and streaming events for real-time updates.

        Args:
            message: Message content to send.
            *args: Implementation-specific arguments.
            **kwargs: Implementation-specific keyword arguments.

        Returns:
            ReturnableAsyncGenerator yielding events and returning response.
        """
        ...

    async def get_messages(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> list[ChatMessage]:
        """Get conversation history.

        Retrieves the complete conversation history in chronological
        order from storage.

        Args:
            *args: Implementation-specific arguments.
            **kwargs: Implementation-specific keyword arguments.

        Returns:
            List of messages in chronological order.
        """
        ...

    async def search_messages(
        self,
        query: str,
        max_results: int | None = None,
        score_threshold: float | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> list[ChatMessage]:
        """Search conversation history.

        Finds messages that are semantically similar to the query text.
        Results can be limited and filtered by similarity score.

        Args:
            query: Text to search for similar messages.
            max_results: Maximum number of messages to return.
            score_threshold: Minimum similarity score (0.0 to 1.0).
            *args: Implementation-specific arguments.
            **kwargs: Implementation-specific keyword arguments.

        Returns:
            List of matching messages sorted by relevance.
        """
        ...

    async def optimize_messages(
        self,
        strategy: OptimizationStrategy,
        *args: Any,
        **kwargs: Any,
    ) -> list[ChatMessage]:
        """Optimize conversation history to reduce context size.

        Applies optimization strategies to reduce context size while
        preserving important information and relationships.

        Args:
            strategy: Type-safe optimization strategy configuration.
            *args: Implementation-specific arguments.
            **kwargs: Implementation-specific keyword arguments.

        Returns:
            Optimized list of messages.
        """
        ...

    async def set_messages(
        self,
        messages: list[ChatMessage],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Set the conversation history.

        Replaces the current conversation history with the provided messages.
        Updates search index and preserves message relationships.

        Args:
            messages: New conversation history to set.
            *args: Implementation-specific arguments.
            **kwargs: Implementation-specific keyword arguments.
        """
        ...

    async def clear_messages(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Clear the conversation history.

        Removes all messages and resets search index.

        Args:
            *args: Implementation-specific arguments.
            **kwargs: Implementation-specific keyword arguments.
        """
        ...


class SwarmChat(Chat[ChatResponse]):
    """In-memory implementation of stateful chat conversations.

    Manages conversation state using in-memory storage while leveraging
    Swarm for message processing. Supports search, optimization, and
    context management through ChatContext.

    The implementation offers:
        - Message persistence with ChatContext
        - Semantic search capabilities
        - Type-safe optimization strategies
        - Agent execution through Swarm
        - Real-time event streaming

    Examples:
        ```python
        # Create chat with components
        chat = SwarmChat()

        # Send message with context
        async for event in chat.send_message(
            "Hello!",
            agent=my_agent,
            context_variables=ContextVariables(user_name="Alice"),
        ):
            if event.type == "agent_response_chunk":
                print(event.chunk.content)

        # Optimize context using window strategy
        messages = await chat.optimize_messages(
            WindowStrategy(
                model="gpt-4o",
                window_size=50,
                preserve_recent=25,
            )
        )
        ```

    Notes:
        - Messages are stored in memory and lost on restart
        - Agent state persists within conversation scope
        - Search uses vector embeddings for semantic matching
        - Optimization strategies are type-safe with discriminated unions
    """

    def __init__(
        self,
        swarm: Swarm | None = None,
        context: ChatContext | None = None,
    ) -> None:
        """Initialize a new chat instance.

        Creates a chat with message storage, search, and optimization
        capabilities. Maintains conversation state and agent execution
        through the provided components.

        Args:
            swarm: Agent execution and event streaming.
            context: Message storage and context management.

        Notes:
            - Components are initialized with defaults if not provided
            - Components should share compatible configurations
            - State is isolated from other chat instances
        """
        self._swarm = swarm or Swarm()
        self._context = context or SwarmChatContext()
        self._last_agent: Agent | None = None

    @override
    @returnable
    async def send_message(
        self,
        message: str,
        *,
        agent: Agent[ContextParams, AgentOutput],
        params: ContextParams = _None,
        final_params_type: type[FinalContextParams] | None = None,
        final_output_type: type[FinalOutputType] | None = None,
    ) -> AsyncStream[SwarmEvent, ChatResponse[FinalContextParams, FinalOutputType]]:
        """Send message and stream response events.

        Processes the message using the specified agent, applying context
        and streaming events for real-time updates. Maintains agent state
        and instruction history within the conversation.

        Args:
            message: Message content to send.
            agent: Agent to process the message.
            params: Context parameters for instruction resolution.
            final_params_type: Optional type for final context parameters.
            final_output_type: Optional type for final output.

        Returns:
            ReturnableAsyncGenerator yielding events and returning ChatResponse.

        Notes:
            System instructions are added when agent or variables change.
        """
        context_messages: list[Message] = []
        messages = await self._context.get_messages()
        messages.append(Message(role="user", content=message))

        stream = self._swarm.stream(
            agent=agent,
            messages=messages,
            params=params,
            final_params_type=final_params_type,
            final_output_type=final_output_type,
        )

        async for event in stream:
            if event.type == "agent_run_start":
                if self._last_agent != event.context.agent:
                    instructions = resolve_agent_instructions(event.context)
                    system_message = Message(role="system", content=instructions)
                    context_messages.append(system_message)
                    self._last_agent = event.context.agent

                context_messages.append(Message(role="user", content=message))

            if event.type == "agent_start":
                if self._last_agent != event.context.agent:
                    system_message = Message(role="system", content=event.instructions)
                    context_messages.append(system_message)
                    self._last_agent = event.context.agent

            if event.type == "agent_complete":
                context_messages.extend(event.new_messages)

            yield YieldItem(event)

        await self._context.add_messages(context_messages)

        result = await stream.get_return_value()
        yield ReturnItem(ChatResponse.from_agent_run_result(result))

    @override
    async def get_messages(self) -> list[ChatMessage]:
        """Get all messages in conversation history.

        Retrieves the complete conversation history in chronological
        order from storage.

        Returns:
            List of messages in chronological order.
        """
        return await self._context.get_chat_messages()

    @override
    async def search_messages(
        self,
        query: str,
        max_results: int | None = None,
        score_threshold: float | None = None,
    ) -> list[ChatMessage]:
        """Search for messages in conversation history.

        Finds messages that are semantically similar to the query text.
        Results are sorted by relevance score.

        Args:
            query: Text to search for similar messages.
            max_results: Maximum number of messages to return.
            score_threshold: Minimum similarity score (0.0 to 1.0).

        Returns:
            List of matching messages sorted by relevance.
        """
        messages = await self._context.search_messages(
            query=query,
            max_results=max_results,
            score_threshold=score_threshold,
        )

        return [ChatMessage.from_message(msg) for msg in messages]

    @override
    async def optimize_messages(self, strategy: OptimizationStrategy) -> list[ChatMessage]:
        """Optimize conversation history to reduce context size.

        Applies optimization strategies to reduce context size while
        preserving important information and relationships.

        Args:
            strategy: Type-safe optimization strategy configuration.

        Returns:
            Optimized list of messages.
        """
        messages = await self._context.optimize_context(strategy)

        return [ChatMessage.from_message(msg) for msg in messages]

    @override
    async def set_messages(self, messages: list[ChatMessage]) -> None:
        """Set the conversation history.

        Replaces the current conversation history with the provided messages.
        Updates search index and preserves message relationships.

        Args:
            messages: New conversation history to set.
        """
        await self._context.clear()
        await self._context.add_chat_messages(messages)

    @override
    async def clear_messages(self) -> None:
        """Clear the conversation history.

        Removes all messages and resets search index.
        """
        await self._context.clear()
        self._last_agent = None
