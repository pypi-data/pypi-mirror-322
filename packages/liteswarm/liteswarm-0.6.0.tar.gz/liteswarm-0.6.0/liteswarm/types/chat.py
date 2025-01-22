# Copyright 2025 GlyphyAI
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import uuid
from datetime import datetime
from typing import Annotated, Any, Generic, Literal

from pydantic import BaseModel, ConfigDict, Discriminator, field_serializer

from liteswarm.types.agent import AgentContext, AgentOutput, ContextParams
from liteswarm.types.llm import AudioResponse, Message, MessageRole, ToolCall
from liteswarm.types.swarm import AgentResponse, AgentRunResult


class ChatMessage(BaseModel):
    """Message type for chat applications with metadata support.

    Extends the base Message type with fields for identification, timestamps,
    and application-specific metadata. Maintains compatibility with base Message
    while adding features needed for chat applications.

    Examples:
        ```python
        # Create from scratch
        message = ChatMessage(
            id="msg_123",
            role="user",
            content="Hello!",
            metadata={"client_id": "web_1"},
        )

        # Convert from base Message
        base_msg = Message(role="assistant", content="Hi!")
        chat_msg = ChatMessage.from_message(
            base_msg,
            metadata={"source": "chat"},
        )
        ```
    """

    id: str
    """Unique message identifier."""

    role: MessageRole
    """Role of the message author."""

    content: str | None = None
    """Text content of the message."""

    tool_calls: list[ToolCall] | None = None
    """Tool calls made in this message."""

    tool_call_id: str | None = None
    """ID of the tool call this message responds to."""

    audio: AudioResponse | None = None
    """Audio response data if available."""

    created_at: datetime = datetime.now()
    """Message creation timestamp."""

    metadata: dict[str, Any] | None = None
    """Application-specific message data."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_attribute_docstrings=True,
        extra="forbid",
    )

    @classmethod
    def from_message(
        cls,
        message: Message,
        *,
        id: str | None = None,
        created_at: datetime | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> "ChatMessage":
        """Create a ChatMessage from a base Message.

        Args:
            message: Base Message to convert.
            id: Optional message identifier.
            created_at: Optional creation timestamp.
            metadata: Optional message metadata.

        Returns:
            New ChatMessage with added fields.
        """
        return cls(
            id=id or str(uuid.uuid4()),
            role=message.role,
            content=message.content,
            tool_calls=message.tool_calls,
            tool_call_id=message.tool_call_id,
            audio=message.audio,
            created_at=created_at or datetime.now(),
            metadata=metadata,
        )

    def to_message(self) -> Message:
        """Convert to base Message type.

        Returns:
            Message without chat-specific fields.
        """
        return Message(
            role=self.role,
            content=self.content,
            tool_calls=self.tool_calls,
            tool_call_id=self.tool_call_id,
            audio=self.audio,
        )

    @field_serializer("created_at")
    def serialize_created_at(self, created_at: datetime) -> str:
        """Serialize created_at field to ISO format."""
        return created_at.isoformat()


class ChatResponse(BaseModel, Generic[ContextParams, AgentOutput]):
    """Complete result of agent execution.

    Contains the final state after all processing, including responses,
    messages, and context updates. Preserves the complete execution
    history and final agent state.
    """

    id: str
    """Unique identifier for the result."""

    final_context: AgentContext[ContextParams, AgentOutput]
    """Agent that produced final response."""

    final_response: AgentResponse[AgentOutput]
    """Final response from agent."""

    agent_responses: list[AgentResponse]
    """Agent responses collected during execution."""

    new_messages: list[Message]
    """Output messages generated during execution."""

    all_messages: list[Message]
    """Complete message history of execution."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_attribute_docstrings=True,
        extra="forbid",
    )

    @classmethod
    def from_agent_run_result(
        cls, result: AgentRunResult[ContextParams, AgentOutput]
    ) -> "ChatResponse[ContextParams, AgentOutput]":
        return cls(
            id=result.id,
            final_context=result.final_context,
            final_response=result.final_response,
            agent_responses=result.agent_responses,
            new_messages=result.new_messages,
            all_messages=result.all_messages,
        )


class WindowStrategy(BaseModel):
    """Configuration for the window-based optimization strategy.

    This strategy keeps a fixed number of most recent messages while
    preserving important context like system messages and tool call pairs.

    Example:
        ```python
        config = WindowStrategy(
            window_size=50,
            preserve_recent=25,
        )
        ```
    """

    type: Literal["window"] = "window"
    """Strategy type identifier."""

    model: str
    """Target language model."""

    window_size: int = 50
    """Number of messages to keep in the window."""

    preserve_recent: int = 25
    """Number of most recent messages to always preserve."""


class TrimStrategy(BaseModel):
    """Configuration for the trim-based optimization strategy.

    This strategy trims older messages while preserving recent ones
    and important context like system messages and tool call pairs.
    """

    type: Literal["trim"] = "trim"
    """Strategy type identifier."""

    model: str
    """Target language model."""

    trim_ratio: float = 0.75
    """Target ratio of max tokens."""


class SummaryStrategy(BaseModel):
    """Configuration for the summary-based optimization strategy.

    This strategy summarizes older messages while preserving recent ones
    and important context like system messages and tool call pairs.

    Example:
        ```python
        config = SummaryStrategy(
            preserve_recent=25,
            summary_model="gpt-4",
            max_summary_tokens=1000,
        )
        ```
    """

    type: Literal["summary"] = "summary"
    """Strategy type identifier."""

    model: str
    """Target language model."""

    preserve_recent: int = 25
    """Number of most recent messages to preserve without summarization."""

    summary_model: str = "gpt-4o"
    """Model to use for generating summaries."""

    max_summary_tokens: int = 1000
    """Maximum tokens to use for summarized content."""


class RAGStrategy(BaseModel):
    """Configuration for the RAG (Retrieval-Augmented Generation) optimization strategy.

    This class defines parameters for controlling how relevant messages are retrieved
    and selected during context optimization. It allows customization of the search
    query, result limits, relevance thresholds, and embedding model selection.

    Example:
        ```python
        config = RAGStrategy(
            query="weather in London",
            max_messages=10,
            score_threshold=0.6,
            embedding_model="text-embedding-3-small",
        )
        ```
    """

    type: Literal["rag"] = "rag"
    """Strategy type identifier."""

    model: str
    """Target language model."""

    query: str
    """The search query used to find relevant messages."""

    max_messages: int | None = None
    """Maximum number of messages to retrieve."""

    score_threshold: float | None = None
    """Minimum similarity score (0-1) for including messages."""

    embedding_model: str | None = None
    """Name of the embedding model to use for semantic search."""


OptimizationStrategy = Annotated[
    WindowStrategy | TrimStrategy | SummaryStrategy | RAGStrategy,
    Discriminator("type"),
]
"""Union type for all supported optimization strategies.

The type field is used as a discriminator to determine which strategy to use.
Each strategy has its own configuration parameters and validation rules.

Example:
    ```python
    # Window strategy
    strategy = WindowStrategy(window_size=50)

    # RAG strategy
    strategy = RAGStrategyConfig(query="context about weather")

    # Summary strategy
    strategy = SummaryStrategy(preserve_recent=25)
    ```
"""
