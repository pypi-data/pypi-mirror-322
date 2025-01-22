# Copyright 2025 GlyphyAI
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from typing import Generic

from typing_extensions import override

from liteswarm.types.agent import AgentOutput
from liteswarm.types.collections import ReturnableAsyncGenerator
from liteswarm.types.events import SwarmEvent
from liteswarm.types.exceptions import SwarmError
from liteswarm.types.swarm import AgentRunResult, ContextParams
from liteswarm.utils.logging import log_verbose


class SwarmStream(
    ReturnableAsyncGenerator[SwarmEvent, AgentRunResult[ContextParams, AgentOutput]],
    Generic[ContextParams, AgentOutput],
):
    """A wrapper around Swarm event stream that adds type validation capabilities.

    SwarmStream provides a type-safe interface for streaming agent execution events
    and retrieving the final result. It validates that the output and parameters
    match their expected types, ensuring type safety throughout execution.

    Type Parameters:
        ContextParams: Type of the context parameters.
        AgentOutput: Type of the agent's output.

    Examples:
        Basic usage:
            ```python
            from liteswarm.types.swarm import Agent
            from liteswarm.types.llm import LLM, Message

            # Create agent
            agent = Agent(
                id="assistant",
                instructions="You are a helpful assistant.",
                llm=LLM(model="gpt-4o"),
            )

            # Stream events
            stream = swarm.stream(agent, messages=messages)
            async for event in stream:
                if event.type == "agent_response_chunk":
                    print(event.chunk.completion.delta.content, end="", flush=True)

            # Get final result
            result = await stream.get_return_value()
            ```

        With type validation:
            ```python
            from pydantic import BaseModel


            class CustomParams(BaseModel):
                mode: str
                options: dict[str, str]


            class CustomOutput(BaseModel):
                result: int
                explanation: str


            stream = swarm.stream(
                agent=agent,
                messages=messages,
                final_params_type=CustomParams,
                final_output_type=CustomOutput,
            )

            result = await stream.get_return_value()
            # Types are validated automatically
            print(result.final_context.params.mode)  # Type-safe access
            print(result.final_response.output.result)  # Type-safe access
            ```

    Notes:
        - Preserves all events from the original stream
        - Validates parameter and output types at completion
        - Provides type-safe access to results
        - Can be configured to warn or error on type mismatches
    """

    def __init__(
        self,
        agen: ReturnableAsyncGenerator[SwarmEvent, AgentRunResult],
        final_params_type: type[ContextParams] | None = None,
        final_output_type: type[AgentOutput] | None = None,
        strict: bool = True,
    ) -> None:
        """Initialize a SwarmStream with event stream and type validation.

        Args:
            agen: The underlying event stream to wrap.
            final_params_type: Optional type to validate context parameters against.
            final_output_type: Optional type to validate agent output against.
            strict: Whether to raise errors on type mismatches (True) or just warn (False).
        """
        super().__init__(agen._agen)
        self._final_params_type = final_params_type
        self._final_output_type = final_output_type
        self._strict = strict

    @override
    async def get_return_value(self) -> AgentRunResult[ContextParams, AgentOutput]:
        """Get the final execution result with type validation.

        Retrieves the final result from the event stream and validates that its
        parameters and output match their expected types if specified. The validation
        ensures type safety when accessing the result's fields.

        Returns:
            Complete execution result with validated types.

        Raises:
            SwarmError: If type validation fails and strict mode is enabled.
            RuntimeError: If the stream completes without a return value.

        Example:
            ```python
            from pydantic import BaseModel


            class CustomParams(BaseModel):
                mode: str
                options: dict[str, str]


            class CustomOutput(BaseModel):
                result: int
                explanation: str


            stream = swarm.stream(
                agent=agent,
                messages=messages,
                final_params_type=CustomParams,
                final_output_type=CustomOutput,
            )

            result = await stream.get_return_value()
            print(result.final_context.params.mode)  # Type-safe access
            print(result.final_response.output.result)  # Type-safe access
            ```
        """
        result = await super().get_return_value()

        if self._final_output_type:
            if not isinstance(result.final_response.output, self._final_output_type):
                message = f"Final output type mismatch: expected {self._final_output_type}, got {type(result.final_response.output)}"
                if self._strict:
                    raise SwarmError(message)

                log_verbose(message, level="WARNING")

        if self._final_params_type:
            if not isinstance(result.final_context.params, self._final_params_type):
                message = f"Final params type mismatch: expected {self._final_params_type}, got {type(result.final_context.params)}"
                if self._strict:
                    raise SwarmError(message)

                log_verbose(message, level="WARNING")

        return result
