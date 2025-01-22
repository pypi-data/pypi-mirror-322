# Copyright 2025 GlyphyAI
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from typing import Any, Protocol

from typing_extensions import override

from liteswarm.chat.summarizer import SwarmChatSummarizer
from liteswarm.chat.vector_index import SwarmMessageVectorIndex
from liteswarm.types.chat import (
    ChatMessage,
    OptimizationStrategy,
    RAGStrategy,
    SummaryStrategy,
    TrimStrategy,
    WindowStrategy,
)
from liteswarm.types.llm import LLM, Message
from liteswarm.utils.messages import filter_tool_call_pairs, trim_messages


class ChatContext(Protocol):
    """Protocol for managing conversation context in chat applications.

    Provides a unified interface for message storage, search, and optimization.
    Implementations can use different storage backends and optimization strategies
    while maintaining consistent context management.

    The protocol is designed to:
        - Store and retrieve messages
        - Search conversation history
        - Optimize context for model limits using type-safe strategies
        - Convert between Message and ChatMessage types

    Examples:
        ```python
        class MyContext(ChatContext):
            def __init__(self) -> None:
                self._messages = []
                self._index = create_vector_index()

            async def add_chat_message(self, message: ChatMessage) -> None:
                self._messages.append(message)
                await self._index.add(message)

            async def add_message(self, message: Message) -> None:
                chat_message = ChatMessage.from_message(message)
                await self.add_chat_message(chat_message)

            async def get_messages(self) -> list[Message]:
                return [msg.to_message() for msg in self._messages]


        # Use custom context
        context = MyContext()
        await context.add_message(Message(role="user", content="Hello!"))
        await context.add_chat_message(
            ChatMessage(
                id="msg1",
                role="assistant",
                content="Hi!",
                created_at=datetime.now(),
            )
        )
        ```

    Notes:
        - All operations are asynchronous
        - Message order must be preserved
        - Implementations should handle both Message and ChatMessage types
        - Optimization uses type-safe strategy configurations
    """

    async def add_message(
        self,
        message: Message,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Add a single base Message to context.

        Converts Message to ChatMessage and stores it.

        Args:
            message: Base Message to store.
            *args: Implementation-specific arguments.
            **kwargs: Implementation-specific keyword arguments.
        """
        ...

    async def add_messages(
        self,
        messages: list[Message],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Add multiple base Messages to context.

        Converts Messages to ChatMessages and stores them.

        Args:
            messages: Base Messages to store.
            *args: Implementation-specific arguments.
            **kwargs: Implementation-specific keyword arguments.
        """
        ...

    async def add_chat_message(
        self,
        message: ChatMessage,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Add a single ChatMessage to context.

        Stores ChatMessage directly and updates search index.

        Args:
            message: ChatMessage to store.
            *args: Implementation-specific arguments.
            **kwargs: Implementation-specific keyword arguments.
        """
        ...

    async def add_chat_messages(
        self,
        messages: list[ChatMessage],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Add multiple ChatMessages to context.

        Stores ChatMessages directly and updates search index.

        Args:
            messages: ChatMessages to store.
            *args: Implementation-specific arguments.
            **kwargs: Implementation-specific keyword arguments.
        """
        ...

    async def get_messages(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> list[Message]:
        """Get all messages as base Message instances.

        Retrieves messages sorted by creation time.
        Returns Message instances for agent compatibility.

        Args:
            *args: Implementation-specific arguments.
            **kwargs: Implementation-specific keyword arguments.

        Returns:
            List of messages in chronological order.
        """
        ...

    async def get_chat_messages(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> list[ChatMessage]:
        """Get all messages as ChatMessage instances.

        Retrieves messages with metadata intact.
        Useful for applications that need message IDs and metadata.

        Args:
            *args: Implementation-specific arguments.
            **kwargs: Implementation-specific keyword arguments.

        Returns:
            List of ChatMessage instances in chronological order.
        """
        ...

    async def search_messages(
        self,
        query: str,
        max_results: int | None = None,
        score_threshold: float | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> list[Message]:
        """Search for semantically similar messages.

        Finds messages that match the query semantically.
        Results are sorted by relevance score.

        Args:
            query: Text to search for.
            max_results: Maximum number of results.
            score_threshold: Minimum similarity score (0.0 to 1.0).
            *args: Implementation-specific arguments.
            **kwargs: Implementation-specific keyword arguments.

        Returns:
            List of matching messages sorted by relevance.
        """
        ...

    async def optimize_context(
        self,
        strategy: OptimizationStrategy,
    ) -> list[Message]:
        """Optimize context for model token limits.

        Applies the specified optimization strategy to reduce context size
        while preserving important information. Each strategy type provides
        its own configuration parameters and validation rules.

        Supported strategies:
            - window: Keep N most recent messages
            - trim: Token-based trimming with ratio control
            - rag: Semantic search with relevance filtering
            - summary: Summarize older messages

        Args:
            strategy: Type-safe optimization strategy configuration.

        Returns:
            Optimized list of messages.

        Example:
            ```python
            # Window strategy
            messages = await context.optimize_context(
                WindowStrategy(
                    model="gpt-4o",
                    window_size=50,
                    preserve_recent=25,
                )
            )

            # RAG strategy
            messages = await context.optimize_context(
                RAGStrategy(
                    model="gpt-4o",
                    query="project requirements",
                    max_messages=20,
                    score_threshold=0.7,
                )
            )
            ```
        """
        ...

    async def clear(self) -> None:
        """Clear all messages from context.

        Removes all stored messages and resets internal state.
        """
        ...


class SwarmChatContext(ChatContext):
    """In-memory implementation of chat context management.

    Provides efficient context management with vector search and
    multiple optimization strategies. Each instance maintains isolated
    conversation state.

    Features:
        - In-memory message storage
        - Vector-based semantic search
        - Type-safe optimization strategies:
            - Window-based: Keep N most recent messages
            - RAG-based: Semantic search with relevance filtering
            - Trim-based: Token-based trimming with ratio control
            - Summary-based: Summarize older messages
        - Automatic message conversion

    Examples:
        ```python
        # Create context
        context = SwarmChatContext()

        # Add messages
        await context.add_message(Message(role="user", content="Hello!"))
        await context.add_message(Message(role="assistant", content="Hi!"))

        # Search messages
        similar = await context.search_messages(
            query="greeting",
            max_results=5,
        )

        # Optimize using window strategy
        optimized = await context.optimize_context(
            WindowStrategy(
                model="gpt-4o",
                window_size=50,
                preserve_recent=25,
            )
        )

        # Optimize using RAG strategy
        optimized = await context.optimize_context(
            RAGStrategy(
                model="gpt-4o",
                query="project requirements",
                max_messages=20,
                score_threshold=0.7,
            )
        )
        ```

    Notes:
        - Messages are stored in memory
        - Search uses text embeddings
        - Optimization strategies are type-safe with discriminated unions
        - Tool calls are kept together during optimization
    """

    def __init__(
        self,
        window_size: int = 50,
        preserve_recent: int = 25,
        embedding_model: str = "text-embedding-3-small",
        embedding_batch_size: int = 16,
    ) -> None:
        """Initialize a new context instance.

        Args:
            window_size: Messages to keep in window strategy.
            preserve_recent: Messages to preserve in summarization.
            embedding_model: Model for computing embeddings.
            embedding_batch_size: Messages to embed in parallel.
        """
        self._messages: list[ChatMessage] = []
        self._vector_index = SwarmMessageVectorIndex(
            embedding_model=embedding_model,
            embedding_batch_size=embedding_batch_size,
        )
        self._summarizer = SwarmChatSummarizer(
            llm=LLM(model="gpt-4o"),
            chunk_size=16,
        )
        self._window_size = window_size
        self._preserve_recent = preserve_recent

    @override
    async def add_message(self, message: Message) -> None:
        """Add a single base Message to context.

        Args:
            message: Base Message to store.
        """
        chat_message = ChatMessage.from_message(message)
        await self.add_chat_message(chat_message)

    @override
    async def add_messages(self, messages: list[Message]) -> None:
        """Add multiple base Messages to context.

        Args:
            messages: Base Messages to store.
        """
        chat_messages = [ChatMessage.from_message(msg) for msg in messages]
        await self.add_chat_messages(chat_messages)

    @override
    async def add_chat_message(self, message: ChatMessage) -> None:
        """Add a single ChatMessage to context.

        Args:
            message: ChatMessage to store.
        """
        self._messages.append(message)

    @override
    async def add_chat_messages(self, messages: list[ChatMessage]) -> None:
        """Add multiple ChatMessages to context.

        Args:
            messages: ChatMessages to store.
        """
        self._messages.extend(messages)

    @override
    async def get_messages(self) -> list[Message]:
        """Get all messages as Message instances.

        Returns:
            List of messages in chronological order.
        """
        messages = await self.get_chat_messages()
        return [msg.to_message() for msg in messages]

    @override
    async def get_chat_messages(self) -> list[ChatMessage]:
        """Get all messages as ChatMessage instances.

        Returns:
            List of ChatMessage instances in chronological order.
        """
        messages = self._messages.copy()
        messages.sort(key=lambda msg: msg.created_at)
        return messages

    @override
    async def search_messages(
        self,
        query: str,
        max_results: int | None = None,
        score_threshold: float | None = None,
        update_index: bool = True,
    ) -> list[Message]:
        """Search for semantically similar messages.

        Args:
            query: Text to search for.
            max_results: Maximum number of results.
            score_threshold: Minimum similarity score.
            update_index: Whether to update the vector index.

        Returns:
            List of matching messages sorted by relevance.
        """
        if update_index:
            messages = await self.get_chat_messages()
            await self._vector_index.index(messages)

        results = await self._vector_index.search(
            query=query,
            max_results=max_results,
            score_threshold=score_threshold,
        )

        return [
            Message(
                role=msg.role,
                content=msg.content,
                tool_calls=msg.tool_calls,
                tool_call_id=msg.tool_call_id,
                audio=msg.audio,
            )
            for msg, _ in results
        ]

    @override
    async def optimize_context(
        self,
        strategy: OptimizationStrategy,
    ) -> list[Message]:
        """Optimize context for model token limits.

        Applies the specified optimization strategy to reduce context size
        while preserving important information. Each strategy type provides
        its own configuration parameters and validation rules.

        Supported strategies:
            - window: Keep N most recent messages
            - trim: Token-based trimming with ratio control
            - rag: Semantic search with relevance filtering
            - summary: Summarize older messages

        Args:
            strategy: Type-safe optimization strategy configuration.

        Returns:
            Optimized list of messages.

        Example:
            ```python
            # Window strategy
            messages = await context.optimize_context(
                WindowStrategy(
                    model="gpt-4o",
                    window_size=50,
                    preserve_recent=25,
                )
            )

            # RAG strategy
            messages = await context.optimize_context(
                RAGStrategy(
                    model="gpt-4o",
                    query="project requirements",
                    max_messages=20,
                    score_threshold=0.7,
                )
            )
            ```
        """
        all_messages = await self.get_messages()

        # Apply the correct optimization strategy on non-system messages
        if strategy.type == "window":
            optimized_non_system = await self._window_strategy(all_messages, strategy)
        elif strategy.type == "trim":
            optimized_non_system = await self._trim_strategy(all_messages, strategy)
        elif strategy.type == "rag":
            optimized_non_system = await self._rag_strategy(all_messages, strategy)
        elif strategy.type == "summary":
            optimized_non_system = await self._summary_strategy(all_messages, strategy)
        else:
            raise ValueError(f"Invalid strategy: {strategy}")

        return optimized_non_system

    async def _window_strategy(
        self,
        messages: list[Message],
        strategy: WindowStrategy,
    ) -> list[Message]:
        """Apply window-based optimization strategy.

        Keeps a fixed number of most recent messages while preserving
        important context like tool call pairs. The window size and
        number of recent messages to preserve are configurable.

        Args:
            messages: Messages to optimize.
            strategy: Window strategy configuration.

        Returns:
            Optimized list of messages.
        """
        if len(messages) <= strategy.window_size:
            return messages

        recent = messages[-strategy.window_size :]
        filtered = filter_tool_call_pairs(recent)
        return trim_messages(filtered, strategy.model)

    async def _trim_strategy(
        self,
        messages: list[Message],
        strategy: TrimStrategy,
    ) -> list[Message]:
        """Apply trim-based optimization strategy.

        Trims messages to fit within model token limits while preserving
        important context. The trim ratio controls how aggressively to
        reduce the context size.

        Args:
            messages: Messages to optimize.
            strategy: Trim strategy configuration.

        Returns:
            Optimized list of messages.
        """
        return trim_messages(
            messages=messages,
            model=strategy.model,
            trim_ratio=strategy.trim_ratio,
        )

    async def _summary_strategy(
        self,
        messages: list[Message],
        strategy: SummaryStrategy,
    ) -> list[Message]:
        """Apply summary-based optimization strategy.

        Summarizes older messages while preserving recent ones and
        important context. Uses a specified model to generate concise
        summaries of older messages.

        Args:
            messages: Messages to optimize.
            strategy: Summary strategy configuration.

        Returns:
            Optimized list of messages.
        """
        if len(messages) <= strategy.preserve_recent:
            return list(messages)

        to_preserve = filter_tool_call_pairs(list(messages[-strategy.preserve_recent :]))
        to_summarize = filter_tool_call_pairs(list(messages[: -strategy.preserve_recent]))

        if not to_summarize:
            return to_preserve

        summary_message = await self._summarizer.summarize(to_summarize)
        combined_messages = [summary_message, *to_preserve]
        return trim_messages(combined_messages, strategy.model)

    async def _rag_strategy(
        self,
        messages: list[Message],
        strategy: RAGStrategy,
    ) -> list[Message]:
        """Apply RAG-based optimization strategy.

        Uses semantic search to find relevant messages based on a query.
        Supports configurable relevance thresholds and embedding models
        for fine-tuned retrieval.

        Args:
            messages: Messages to optimize.
            strategy: RAG strategy configuration.

        Returns:
            Optimized list of messages.
        """
        relevant_messages = await self.search_messages(
            query=strategy.query,
            max_results=strategy.max_messages,
            score_threshold=strategy.score_threshold,
        )

        if not relevant_messages:
            return trim_messages(messages, strategy.model)

        trimmed_messages = trim_messages(messages, strategy.model, trim_ratio=0.5)
        combined_messages = [*trimmed_messages, *relevant_messages]
        return combined_messages

    @override
    async def clear(self) -> None:
        """Clear all messages and reset index."""
        self._messages.clear()
        await self._vector_index.clear()
