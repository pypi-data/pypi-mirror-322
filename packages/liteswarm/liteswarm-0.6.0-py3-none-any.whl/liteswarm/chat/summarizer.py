# Copyright 2025 GlyphyAI
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import asyncio
from typing import Any, Protocol

from litellm import acompletion
from typing_extensions import override

from liteswarm.types.llm import LLM
from liteswarm.types.swarm import Message
from liteswarm.utils.logging import log_verbose
from liteswarm.utils.messages import dump_messages, filter_tool_call_pairs

SUMMARIZER_SYSTEM_PROMPT = """\
You are a precise conversation summarizer that distills complex interactions into essential points.

Your summaries must capture:
- Key decisions and outcomes
- Essential context needed for future interactions
- Tool calls and their results
- Important user requirements or constraints

Focus on factual information and exclude:
- Greetings and acknowledgments
- Routine interactions
- Redundant information
- Conversational fillers

Be extremely concise while preserving all critical details.\
"""

SUMMARIZER_USER_PROMPT = """\
Create a 2-3 sentence summary of this conversation segment that captures only:
1. Key decisions and actions taken
2. Essential context for future reference
3. Important tool interactions and their outcomes

Be direct and factual. Exclude any unnecessary details or pleasantries.\
"""


class ChatSummarizer(Protocol):
    """Protocol for conversation summarization.

    Defines interface for creating concise summaries of conversation history
    while preserving critical information. Implementations should focus on
    key decisions, tool interactions, and essential context.

    Examples:
        ```python
        class MySummarizer(ChatSummarizer):
            async def summarize(
                self,
                messages: list[Message],
            ) -> Message:
                # Extract key points and create summary
                content = self._extract_key_points(messages)
                return Message(role="assistant", content=content)
        ```
    """

    async def summarize(
        self,
        messages: list[Message],
        *args: Any,
        **kwargs: Any,
    ) -> Message:
        """Summarize conversation messages.

        Args:
            messages: List of messages to summarize.
            *args: Implementation-specific arguments.
            **kwargs: Implementation-specific keyword arguments.

        Returns:
            Message containing the summary.
        """
        ...


class SwarmChatSummarizer(ChatSummarizer):
    """LLM-based implementation of conversation summarization.

    Uses language models to create focused summaries that capture key information
    while removing unnecessary details. Preserves tool calls and their results
    in proper context.

    Examples:
        ```python
        summarizer = SwarmChatSummarizer(
            llm=LLM(model="gpt-4o"),
            chunk_size=10,
        )

        summary = await summarizer.summarize(messages)
        print(summary.content)  # Concise summary of key points
        ```
    """

    def __init__(self, llm: LLM | None = None, chunk_size: int = 10) -> None:
        """Initialize summarizer with configuration.

        Args:
            llm: LLM config for summarization.
            chunk_size: Messages per summary chunk.
        """
        self._llm = llm or LLM(model="gpt-4o")
        self._chunk_size = chunk_size

    def _create_message_chunks(self, messages: list[Message]) -> list[list[Message]]:
        """Create chunks of messages for summarization.

        Groups messages into chunks while preserving tool call pairs and
        maintaining proper message relationships. Ensures that tool calls
        and their results stay together.

        Args:
            messages: List of messages to chunk.

        Returns:
            List of message chunks ready for summarization.
        """
        if not messages:
            return []

        chunks: list[list[Message]] = []
        current_chunk: list[Message] = []
        pending_tool_calls: dict[str, Message] = {}

        def add_chunk() -> None:
            if current_chunk:
                filtered_chunk = filter_tool_call_pairs(current_chunk)
                if filtered_chunk:
                    chunks.append(filtered_chunk)
                current_chunk.clear()
                pending_tool_calls.clear()

        def add_chunk_if_needed() -> None:
            if len(current_chunk) >= self._chunk_size and not pending_tool_calls:
                add_chunk()

        for message in messages:
            add_chunk_if_needed()

            if message.role == "assistant" and message.tool_calls:
                current_chunk.append(message)
                for tool_call in message.tool_calls:
                    if tool_call.id:
                        pending_tool_calls[tool_call.id] = message

            elif message.role == "tool" and message.tool_call_id:
                current_chunk.append(message)
                pending_tool_calls.pop(message.tool_call_id, None)
                add_chunk_if_needed()

            else:
                current_chunk.append(message)
                add_chunk_if_needed()

        if current_chunk:
            add_chunk()

        return chunks

    async def _summarize_chunk(self, messages: list[Message]) -> str | None:
        """Create concise summary of message chunk.

        Uses LLM to generate focused summary of key information.

        Args:
            messages: List of messages to summarize.

        Returns:
            Summary of the message chunk.
        """
        log_verbose(
            f"Summarizing chunk of {len(messages)} messages",
            level="DEBUG",
        )

        system_message = Message(role="system", content=SUMMARIZER_SYSTEM_PROMPT)
        user_message = Message(role="user", content=SUMMARIZER_USER_PROMPT)

        input_messages: list[Message] = [
            system_message,
            *messages,
            user_message,
        ]

        completion_kwargs: dict[str, Any] = {
            **self._llm.model_dump(exclude_none=True),
            "messages": dump_messages(input_messages),
        }

        response = await acompletion(**completion_kwargs)
        summary = response.choices[0].message.content
        if not summary:
            return None

        log_verbose(
            f"Generated summary of length {len(summary)}",
            level="DEBUG",
        )

        return summary

    @override
    async def summarize(self, messages: list[Message]) -> Message:
        """Summarize conversation while preserving key information.

        Creates concise summaries of message chunks and combines them
        into a single summary message.

        Args:
            messages: List of messages to process.

        Returns:
            Message containing the complete summary.
        """
        chunks = self._create_message_chunks(messages)
        summarize_tasks = [self._summarize_chunk(chunk) for chunk in chunks]
        summarize_results = await asyncio.gather(*summarize_tasks)
        summaries = [summary for summary in summarize_results if summary is not None]

        summary_message = Message(
            role="assistant",
            content=f"Previous conversation summary:\n{' '.join(summaries)}",
        )

        return summary_message
