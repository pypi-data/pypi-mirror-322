# Copyright 2025 GlyphyAI
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import argparse
import json
import shlex
import sys
from typing import Any, NoReturn

from litellm import token_counter
from pydantic import TypeAdapter
from typing_extensions import override

from liteswarm.chat import SwarmChat
from liteswarm.chat.chat import Chat
from liteswarm.core.swarm import Swarm
from liteswarm.repl.event_handler import ConsoleEventHandler
from liteswarm.types.agent import Agent, AgentOutput, ContextParams
from liteswarm.types.chat import (
    ChatMessage,
    ChatResponse,
    OptimizationStrategy,
    RAGStrategy,
    SummaryStrategy,
    TrimStrategy,
    WindowStrategy,
)
from liteswarm.types.llm import ResponseCost, Usage
from liteswarm.types.typing import _None
from liteswarm.utils.logging import LogLevel, log_verbose
from liteswarm.utils.logging import set_verbose as liteswarm_enable_logging
from liteswarm.utils.misc import prompt

ChatMessageList = TypeAdapter(list[ChatMessage])
"""Type adapter to (de)serialize lists of ChatMessage objects."""


class ReplArgumentParser(argparse.ArgumentParser):
    """Custom argument parser that raises exceptions instead of exiting.

    Designed for interactive use in REPL environments where program termination
    on error is undesirable.
    """

    @override
    def error(self, message: str) -> NoReturn:
        """Raise an ArgumentError instead of exiting.

        Args:
            message: Error message to include in the exception.
        """
        raise argparse.ArgumentError(None, message)


class AgentRepl:
    """Interactive REPL for agent-based conversations.

    Provides a command-line interface for interacting with agents through a
    Read-Eval-Print Loop (REPL). Features include conversation management,
    command-based control, message storage, usage tracking, and context
    optimization.

    Example:
        ```python
        agent = Agent(
            id="helper",
            instructions="You are a helpful assistant.",
            llm=LLM(model="gpt-4o"),
        )

        repl = AgentRepl(
            agent=agent,
            include_usage=True,
            include_cost=True,
        )

        await repl.run()
        ```

    Notes:
        - The REPL runs until explicitly terminated
        - Supports context optimization for long conversations
        - Maintains conversation context between queries
        - Handles interrupts and errors gracefully
    """

    def __init__(
        self,
        agent: Agent[ContextParams, AgentOutput],
        params: ContextParams = _None,
        chat: Chat[ChatResponse] | None = None,
        include_usage: bool = False,
        include_cost: bool = False,
        max_iterations: int = sys.maxsize,
    ) -> None:
        """Initialize REPL with agent and configuration.

        Args:
            agent: Initial agent for conversations.
            params: Initial context parameters.
            chat: Custom chat implementation.
            include_usage: Whether to track token usage.
            include_cost: Whether to track costs.
            max_iterations: Maximum conversation turns.
        """
        # Public configuration
        self.chat = chat or SwarmChat(
            swarm=Swarm(
                include_usage=include_usage,
                include_cost=include_cost,
                max_iterations=max_iterations,
            ),
        )

        # Internal state (private)
        self._event_handler = ConsoleEventHandler()
        self._accumulated_usage: Usage | None = None
        self._accumulated_cost: ResponseCost | None = None
        self._agent: Agent[Any, Any] = agent
        self._params: Any = params

    async def _print_welcome(self) -> None:
        """Display welcome message and available commands."""
        print("\n🤖 Agent REPL")
        print(f"Starting with agent: {self._agent.id}")
        print("\nCommands:")
        print("  /exit    - Exit the REPL")
        print("  /help    - Show this help message")
        print("  /clear   - Clear conversation memory")
        print("  /history - Show conversation messages")
        print("  /stats   - Show conversation statistics")
        print("  /save    - Save conversation memory to file")
        print("  /load    - Load conversation memory from file")
        print("  /optimize --strategy <strategy> [--model <model>] - Optimize context")
        print("           strategies: summarize, window, compress")
        print("  /find --query <query> [--count <n>] - Find relevant messages")
        print("\nEnter your queries and press Enter. Use commands above to control the REPL.")
        print("\n" + "=" * 50 + "\n")

    async def _print_history(self) -> None:
        """Display conversation message history.

        Shows all non-system messages chronologically.
        """
        print("\n📝 Conversation Messages:")
        messages = await self.chat.get_messages()
        for msg in messages:
            if msg.role != "system":
                content = msg.content or "[No content]"
                print(f"\n[{msg.role}]: {content}")
        print("\n" + "=" * 50 + "\n")

    async def _print_stats(self) -> None:
        """Display conversation statistics.

        Shows message counts, token usage, and costs if enabled.
        """
        messages = await self.chat.get_messages()
        print("\n📊 Conversation Statistics:")
        print(f"Message count: {len(messages)} messages")

        if self._accumulated_usage:
            print("\nAccumulated Token Usage:")
            print(f"  Prompt tokens: {self._accumulated_usage.prompt_tokens or 0:,}")
            print(f"  Completion tokens: {self._accumulated_usage.completion_tokens or 0:,}")
            print(f"  Total tokens: {self._accumulated_usage.total_tokens or 0:,}")

            if self._accumulated_usage.prompt_tokens_details:
                print("\nPrompt Token Details:")
                prompt_token_details = self._accumulated_usage.prompt_tokens_details
                items = prompt_token_details.model_dump().items()
                for key, value in items:
                    if value is not None:
                        print(f"  {key}: {value:,}")

            if self._accumulated_usage.completion_tokens_details:
                print("\nCompletion Token Details:")
                completion_token_details = self._accumulated_usage.completion_tokens_details
                items = completion_token_details.model_dump().items()
                for key, value in items:
                    if value is not None:
                        print(f"  {key}: {value:,}")

        if self._accumulated_cost:
            prompt_cost = self._accumulated_cost.prompt_tokens_cost or 0
            completion_cost = self._accumulated_cost.completion_tokens_cost or 0
            total_cost = prompt_cost + completion_cost

            print("\nAccumulated Response Cost:")
            print(f"  Prompt tokens: ${prompt_cost:.6f}")
            print(f"  Completion tokens: ${completion_cost:.6f}")
            print(f"  Total cost: ${total_cost:.6f}")

        print("\nActive Agent:")
        print(f"  ID: {self._agent.id}")
        print(f"  Model: {self._agent.llm.model}")
        print(f"  Tools: {len(self._agent.tools)} available")

        print("\n" + "=" * 50 + "\n")

    async def _save_history(self, filename: str = "conversation_memory.json") -> None:
        """Save conversation memory to JSON file.

        Args:
            filename: Target file path.
        """
        messages = await self.chat.get_messages()
        memory = {"messages": ChatMessageList.dump_python(messages, exclude_none=True)}

        with open(filename, "w") as f:
            json.dump(memory, f, indent=2)

        print(f"\n📤 Conversation memory saved to {filename}")
        print(f"Messages: {len(memory['messages'])} messages")

    async def _load_history(self, filename: str = "conversation_memory.json") -> None:
        """Load conversation memory from JSON file.

        Args:
            filename: Source file path.
        """
        try:
            with open(filename) as f:
                memory: dict[str, Any] = json.load(f)

            messages = ChatMessageList.validate_python(memory.get("messages", []))
            await self.chat.set_messages(messages)

            print(f"\n📥 Conversation memory loaded from {filename}")
            print(f"Messages: {len(messages)} messages")

            messages_dump = [msg.model_dump() for msg in messages if msg.role != "system"]
            prompt_tokens = token_counter(model=self._agent.llm.model, messages=messages_dump)
            print(f"Token count: {prompt_tokens:,}")

        except FileNotFoundError:
            print(f"\n❌ Memory file not found: {filename}")
        except json.JSONDecodeError:
            print(f"\n❌ Invalid JSON format in memory file: {filename}")
        except Exception as e:
            print(f"\n❌ Error loading memory: {str(e)}")

    async def _clear_history(self) -> None:
        """Clear conversation memory and reset REPL state."""
        self._accumulated_usage = None
        self._accumulated_cost = None
        await self.chat.clear_messages()
        print("\n🧹 Conversation memory cleared")

    def _parse_command_args(
        self,
        parser: ReplArgumentParser,
        args_str: str,
        join_args: list[str] | None = None,
    ) -> argparse.Namespace | None:
        """Parse command arguments with error handling.

        Args:
            parser: The argument parser to use.
            args_str: Raw argument string to parse.
            join_args: List of argument names whose values should be joined.

        Returns:
            Parsed arguments or None if parsing failed.
        """
        try:
            cleaned_args = []
            for arg in shlex.split(args_str):
                if "=" in arg:
                    key, value = arg.split("=", 1)
                    cleaned_args.extend([key, value])
                else:
                    cleaned_args.append(arg)

            parsed = parser.parse_args(cleaned_args)

            if join_args:
                for arg_name in join_args:
                    arg_value = getattr(parsed, arg_name, None)
                    if isinstance(arg_value, list):
                        setattr(parsed, arg_name, " ".join(arg_value))

            return parsed

        except argparse.ArgumentError as e:
            print(f"\n❌ {str(e)}")
            parser.print_usage()
            return None

        except argparse.ArgumentTypeError as e:
            print(f"\n❌ {str(e)}")
            parser.print_usage()
            return None

        except (ValueError, Exception) as e:
            print(f"\n❌ Invalid command format: {str(e)}")
            parser.print_usage()
            return None

    def _create_optimize_parser(self) -> ReplArgumentParser:
        """Create argument parser for the optimize command."""
        parser = ReplArgumentParser(
            prog="/optimize",
            description="Optimize conversation context using specified strategy",
            add_help=False,
        )
        parser.add_argument(
            "--strategy",
            "-s",
            required=True,
            choices=["window", "trim", "summary", "rag"],
            help="Optimization strategy to use",
        )
        parser.add_argument(
            "--model",
            "-m",
            help="Model to optimize for (defaults to agent's model)",
        )
        parser.add_argument(
            "--query",
            "-q",
            nargs="+",
            help="Query to use for RAG strategy",
        )
        parser.add_argument(
            "--window-size",
            "-w",
            type=int,
            default=50,
            help="Window size for window strategy",
        )
        parser.add_argument(
            "--preserve-recent",
            "-p",
            type=int,
            default=25,
            help="Number of recent messages to preserve",
        )
        parser.add_argument(
            "--trim-ratio",
            "-r",
            type=float,
            default=0.75,
            help="Trim ratio for trim strategy",
        )
        parser.add_argument(
            "--score-threshold",
            "-t",
            type=float,
            default=0.5,
            help="Minimum similarity score for RAG strategy",
        )
        parser.add_argument(
            "--max-messages",
            "-n",
            type=int,
            help="Maximum number of messages for RAG strategy",
        )
        return parser

    def _create_find_parser(self) -> ReplArgumentParser:
        """Create argument parser for the find command."""
        parser = ReplArgumentParser(
            prog="/find",
            description="Find messages relevant to the given query",
            add_help=False,
        )
        parser.add_argument(
            "--query",
            "-q",
            required=True,
            nargs="+",
            help="Search query",
        )
        parser.add_argument(
            "--count",
            "-n",
            type=int,
            help="Maximum number of messages to return",
        )
        parser.add_argument(
            "--threshold",
            "-t",
            type=float,
            default=0.5,
            help="Minimum similarity score (0.0 to 1.0)",
        )
        return parser

    async def _handle_command(self, command: str) -> bool:
        """Handle REPL commands and return whether to exit.

        Args:
            command: The command to handle.

        Returns:
            True if the REPL should exit, False otherwise.
        """
        parts = shlex.split(command)
        cmd = parts[0].lower()
        args = " ".join(parts[1:])

        match cmd:
            case "/exit":
                print("\n👋 Goodbye!")
                return True
            case "/help":
                await self._print_welcome()
            case "/clear":
                await self._clear_history()
            case "/history":
                await self._print_history()
            case "/stats":
                await self._print_stats()
            case "/save":
                await self._save_history()
            case "/load":
                await self._load_history()
            case "/optimize":
                await self._optimize_context(args)
            case "/find":
                await self._find_relevant(args)
            case _:
                print("\n❌ Unknown command. Type /help for available commands.")

        return False

    def _update_usage(self, new_usage: Usage | None) -> None:
        """Update accumulated usage statistics.

        Args:
            new_usage: New usage data to add.
        """
        if not new_usage:
            return

        if not self._accumulated_usage:
            self._accumulated_usage = new_usage
            return

        self._accumulated_usage.prompt_tokens = new_usage.prompt_tokens
        self._accumulated_usage.completion_tokens += new_usage.completion_tokens
        self._accumulated_usage.total_tokens = (
            self._accumulated_usage.prompt_tokens + self._accumulated_usage.completion_tokens
        )

        if new_usage.prompt_tokens_details:
            self._accumulated_usage.prompt_tokens_details = new_usage.prompt_tokens_details

        if new_usage.completion_tokens_details:
            if not self._accumulated_usage.completion_tokens_details:
                self._accumulated_usage.completion_tokens_details = new_usage.completion_tokens_details
            else:
                completion_token_details = self._accumulated_usage.completion_tokens_details
                items = completion_token_details.model_dump().items()
                for key, value in items:
                    if value is not None:
                        current = getattr(self._accumulated_usage.completion_tokens_details, key) or 0
                        setattr(self._accumulated_usage.completion_tokens_details, key, current + value)

    def _update_cost(self, new_cost: ResponseCost | None) -> None:
        """Update accumulated cost statistics.

        Args:
            new_cost: New cost data to add.
        """
        if not new_cost:
            return

        if not self._accumulated_cost:
            self._accumulated_cost = new_cost
            return

        self._accumulated_cost.prompt_tokens_cost = new_cost.prompt_tokens_cost
        self._accumulated_cost.completion_tokens_cost += new_cost.completion_tokens_cost

    async def _process_query(self, query: str) -> None:
        """Process user query through agent system.

        Args:
            query: User's input query.
        """
        try:
            stream = self.chat.send_message(
                query,
                agent=self._agent,
                params=self._params,
            )

            async for event in stream:
                self._event_handler.on_event(event)

            result = await stream.get_return_value()
            self._agent = result.final_context.agent
            self._params = result.final_context.params

            for response in result.agent_responses:
                if response.usage:
                    self._update_usage(response.usage)
                if response.response_cost:
                    self._update_cost(response.response_cost)

            print("\n" + "=" * 50 + "\n")
        except Exception as e:
            print(f"\n❌ Error processing query: {str(e)}", file=sys.stderr)

    async def _optimize_context(self, args: str) -> None:
        """Optimize conversation context with specified strategy.

        Args:
            args: Raw command arguments string.
        """
        try:
            parser = self._create_optimize_parser()
            parsed = self._parse_command_args(parser, args, join_args=["query"])
            if not parsed:
                print("\nUsage examples:")
                print("  /optimize -s window -w 50 -p 25")
                print("  /optimize -s trim -r 0.75")
                print("  /optimize -s summary -p 25")
                print("  /optimize -s rag -q 'search query' -t 0.7 -n 20")
                return

            log_verbose(f"Optimizing context with {parsed}")

            messages = await self.chat.get_messages()
            if not messages:
                print("\n❌ No messages to optimize")
                return

            model = parsed.model or self._agent.llm.model
            strategy_type = parsed.strategy
            strategy: OptimizationStrategy

            # Create the appropriate strategy based on type
            if strategy_type == "window":
                strategy = WindowStrategy(
                    model=model,
                    window_size=parsed.window_size,
                    preserve_recent=parsed.preserve_recent,
                )
            elif strategy_type == "trim":
                strategy = TrimStrategy(
                    model=model,
                    trim_ratio=parsed.trim_ratio,
                )
            elif strategy_type == "summary":
                strategy = SummaryStrategy(
                    model=model,
                    preserve_recent=parsed.preserve_recent,
                )
            elif strategy_type == "rag":
                if not parsed.query:
                    print("\n❌ Query is required for RAG strategy")
                    return

                strategy = RAGStrategy(
                    model=model,
                    query=" ".join(parsed.query),
                    max_messages=parsed.max_messages,
                    score_threshold=parsed.score_threshold,
                )
            else:
                print(f"\n❌ Invalid strategy: {strategy_type}")
                return

            optimized = await self.chat.optimize_messages(strategy)
            await self.chat.set_messages(optimized)

            print(f"\n✨ Context optimized using {strategy_type} strategy")
            print(f"Messages: {len(messages)} → {len(optimized)}")

        except Exception as e:
            print(f"\n❌ Error optimizing context: {str(e)}")
            print("\nUsage examples:")
            print("  /optimize -s window -w 50 -p 25")
            print("  /optimize -s trim -r 0.75")
            print("  /optimize -s summary -p 25")
            print("  /optimize -s rag -q 'search query' -t 0.7 -n 20")

    async def _find_relevant(self, args: str) -> None:
        """Find messages relevant to given query.

        Args:
            args: Raw command arguments string.
        """
        try:
            parser = self._create_find_parser()
            parsed = self._parse_command_args(parser, args, join_args=["query"])
            if not parsed:
                print("\nUsage examples:")
                print('  /find --query "calendar view" --count 5')
                print('  /find -q "search term" -n 3 -t 0.7')
                print("  /find --query calendar view --threshold 0.8")
                print("  /find -q calendar view -n 3 --threshold 0.6")
                return

            messages = await self.chat.search_messages(
                query=parsed.query,
                max_results=parsed.count,
                score_threshold=parsed.threshold,
            )

            if not messages:
                print("\n❌ No relevant messages found")
                return

            print(f"\n🔍 Found {len(messages)} relevant messages:")
            for msg in messages:
                if msg.role != "system":
                    content = msg.content or "[No content]"
                    print(f"\n[{msg.role}]: {content}")

            print("\n" + "=" * 50 + "\n")

        except Exception as e:
            print(f"\n❌ Error finding relevant messages: {str(e)}")
            print("\nUsage examples:")
            print('  /find --query "calendar view" --count 5')
            print('  /find -q "search term" -n 3 -t 0.7')
            print("  /find --query calendar view --threshold 0.8")
            print("  /find -q calendar view -n 3 --threshold 0.6")

    async def run(self) -> NoReturn:
        """Run REPL loop until explicitly terminated."""
        await self._print_welcome()

        while True:
            try:
                user_input = await prompt("\n🗣️  Enter your query: ")

                if not user_input:
                    continue

                if user_input.startswith("/"):
                    log_verbose(f"Handling command: {user_input}")
                    if await self._handle_command(user_input):
                        sys.exit(0)

                    continue

                await self._process_query(user_input)

            except KeyboardInterrupt:
                print("\n\n👋 Interrupted by user. Goodbye!")
                sys.exit(0)
            except EOFError:
                print("\n\n👋 EOF received. Goodbye!")
                sys.exit(0)
            except Exception as e:
                print(f"\n❌ Unexpected error: {str(e)}", file=sys.stderr)
                continue


async def start_repl(
    agent: Agent[ContextParams, AgentOutput],
    params: ContextParams = _None,
    chat: Chat[ChatResponse] | None = None,
    include_usage: bool = False,
    include_cost: bool = False,
    max_iterations: int = sys.maxsize,
    enable_logging: bool = True,
    log_level: LogLevel = "INFO",
) -> NoReturn:
    """Start interactive REPL session.

    Args:
        agent: Initial agent for conversations.
        params: Initial context parameters.
        chat: Custom chat implementation.
        include_usage: Whether to track token usage.
        include_cost: Whether to track costs.
        max_iterations: Maximum conversation turns.
        enable_logging: Whether to enable logging.
        log_level: Log level for logging.

    Example:
        ```python
        agent = Agent(
            id="helper",
            instructions="You are a helpful assistant.",
            llm=LLM(model="gpt-4o"),
        )

        await start_repl(agent=agent, include_usage=True)
        ```
    """
    if enable_logging:
        liteswarm_enable_logging(default_level=log_level)

    repl = AgentRepl(
        agent=agent,
        params=params,
        chat=chat,
        include_usage=include_usage,
        include_cost=include_cost,
        max_iterations=max_iterations,
    )

    await repl.run()
