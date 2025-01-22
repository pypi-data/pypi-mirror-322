# Copyright 2025 GlyphyAI
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from typing import Any

from liteswarm.types.agent import Agent, AgentContext


class SwarmError(Exception):
    """Base exception class for all Swarm-related errors.

    Provides a common ancestor for all custom exceptions in the system,
    enabling unified error handling and logging of Swarm operations.
    """

    def __init__(
        self,
        message: str,
        original_error: Exception | None = None,
    ) -> None:
        """Initialize a new SwarmError.

        Args:
            message: Human-readable error description.
            original_error: Optional underlying exception that caused the failure.
        """
        super().__init__(message)
        self.original_error = original_error


class CompletionError(SwarmError):
    """Exception raised when LLM completion fails permanently.

    Indicates that the language model API call failed and exhausted
    all retry attempts. Preserves the original error for debugging
    and error reporting.
    """

    def __init__(
        self,
        message: str,
        original_error: Exception | None = None,
    ) -> None:
        """Initialize a new CompletionError.

        Args:
            message: Human-readable error description.
            original_error: Optional underlying exception that caused the failure.
        """
        super().__init__(message, original_error)


class ContextLengthError(SwarmError):
    """Exception raised when input exceeds model's context limit.

    Occurs when the combined length of conversation history and new
    input exceeds the model's maximum context window, even after
    attempting context reduction strategies.
    """

    def __init__(
        self,
        message: str,
        model: str | None = None,
        current_length: int | None = None,
        max_length: int | None = None,
        original_error: Exception | None = None,
    ) -> None:
        """Initialize a new ContextLengthError.

        Args:
            message: Human-readable error description.
            model: Model that exceeded the context limit.
            current_length: Current context length that exceeded the limit.
            max_length: Maximum allowed context length.
            original_error: Optional underlying exception that caused the failure.
        """
        super().__init__(message, original_error)
        self.model = model
        self.current_length = current_length
        self.max_length = max_length


class FinalAgentMismatchError(SwarmError):
    """Raised when the final agent in the execution flow doesn't match the expected agent.

    This error indicates that the execution ended with a different agent than what was
    specified as the final_agent. Users can catch this error to handle the mismatch,
    for example by running the expected final agent with the accumulated context.
    """

    def __init__(
        self,
        message: str,
        expected_agent: Agent[Any, Any],
        actual_agent: Agent[Any, Any],
        final_context: AgentContext[Any, Any],
        original_error: Exception | None = None,
    ) -> None:
        """Initialize a new FinalAgentMismatchError.

        Args:
            message: Human-readable error description.
            expected_agent: The agent that was expected to be final.
            actual_agent: The agent that actually completed the execution.
            final_context: The final execution context containing messages and params.
            original_error: Optional underlying exception that caused the failure.
        """
        super().__init__(message, original_error)
        self.expected_agent = expected_agent
        self.actual_agent = actual_agent
        self.final_context = final_context


class MaxAgentSwitchesError(SwarmError):
    """Exception raised when too many agent switches occur.

    Indicates potential infinite loops or excessive agent switches.
    This error helps prevent scenarios where agents continuously pass control
    between each other without making progress.
    """

    def __init__(
        self,
        message: str,
        switch_count: int,
        max_switches: int,
        switch_history: list[str] | None = None,
        original_error: Exception | None = None,
    ) -> None:
        """Initialize a new MaxAgentSwitchesError.

        Args:
            message: Human-readable error description.
            switch_count: Number of switches that occurred.
            max_switches: Maximum allowed switches.
            switch_history: Optional list of agent IDs in switch order.
            original_error: Optional underlying exception.
        """
        super().__init__(message, original_error)
        self.switch_count = switch_count
        self.max_switches = max_switches
        self.switch_history = switch_history


class MaxResponseContinuationsError(SwarmError):
    """Exception raised when response needs too many continuations.

    Occurs when an agent's response exceeds length limits and requires more
    continuations than allowed. This helps prevent scenarios where responses
    grow indefinitely without reaching a natural conclusion.
    """

    def __init__(
        self,
        message: str,
        continuation_count: int,
        max_continuations: int,
        total_tokens: int | None = None,
        original_error: Exception | None = None,
    ) -> None:
        """Initialize a new MaxResponseContinuationsError.

        Args:
            message: Human-readable error description.
            continuation_count: Number of continuations attempted.
            max_continuations: Maximum allowed continuations.
            total_tokens: Optional total tokens generated.
            original_error: Optional underlying exception.
        """
        super().__init__(message, original_error)
        self.continuation_count = continuation_count
        self.max_continuations = max_continuations
        self.total_tokens = total_tokens


class RetryError(SwarmError):
    """Exception raised when retry mechanism fails.

    Indicates that all retry attempts have been exhausted without success.
    This error provides detailed information about the retry process,
    including attempt counts, timing, and the original error that
    triggered retries.
    """

    def __init__(
        self,
        message: str,
        attempts: int,
        total_duration: float,
        backoff_strategy: dict[str, float],
        original_error: Exception,
    ) -> None:
        """Initialize a new RetryError.

        Args:
            message: Human-readable error description.
            attempts: Number of retry attempts made.
            total_duration: Total time spent retrying in seconds.
            backoff_strategy: Dictionary with retry settings.
            original_error: The underlying exception that caused retries.
        """
        super().__init__(message, original_error)
        self.attempts = attempts
        self.total_duration = total_duration
        self.backoff_strategy = backoff_strategy


class SwarmTeamError(SwarmError):
    """Base exception class for SwarmTeam-related errors.

    Provides a common ancestor for all SwarmTeam exceptions, enabling unified error
    handling for team operations like planning, task execution, and response processing.
    """

    def __init__(
        self,
        message: str,
        original_error: Exception | None = None,
    ) -> None:
        """Initialize a new SwarmTeamError.

        Args:
            message: Human-readable error description.
            original_error: Optional underlying exception that caused the failure.
        """
        super().__init__(message, original_error)
