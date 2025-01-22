"""Conversation management for LLMling agent."""

from __future__ import annotations

from collections import deque
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime
import tempfile
from typing import TYPE_CHECKING, Any, Literal, Self, overload
from uuid import UUID, uuid4

from llmling import BasePrompt, PromptMessage, StaticPrompt
from llmling.config.models import BaseResource
from psygnal import Signal
from pydantic_ai.messages import ModelRequest, SystemPromptPart, UserPromptPart
from toprompt import AnyPromptType, to_prompt
from upath import UPath

from llmling_agent.log import get_logger
from llmling_agent.models.messages import ChatMessage
from llmling_agent.models.session import SessionQuery
from llmling_agent_providers.pydanticai.utils import (
    convert_model_message,
    format_part,
    get_message_role,
    to_model_message,
)


if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Coroutine, Sequence
    from types import TracebackType

    from llmling.config.models import Resource
    from llmling.prompts import PromptType
    from pydantic_ai.messages import ModelMessage

    from llmling_agent.agent.agent import Agent
    from llmling_agent.common_types import MessageRole, SessionIdType, StrPath

logger = get_logger(__name__)

OverrideMode = Literal["replace", "append"]
type PromptInput = str | BasePrompt


def _to_base_prompt(prompt: PromptInput) -> BasePrompt:
    """Convert input to BasePrompt instance."""
    if isinstance(prompt, str):
        msg = PromptMessage(role="system", content=prompt)
        return StaticPrompt(
            name="System prompt", description="System prompt", messages=[msg]
        )
    return prompt


class ConversationManager:
    """Manages conversation state and system prompts."""

    @dataclass(frozen=True)
    class HistoryCleared:
        """Emitted when chat history is cleared."""

        session_id: str
        timestamp: datetime = field(default_factory=datetime.now)

    history_cleared = Signal(HistoryCleared)

    def __init__(
        self,
        agent: Agent[Any],
        session: SessionIdType | SessionQuery = None,
        *,
        resources: Sequence[Resource | PromptType | str] = (),
    ):
        """Initialize conversation manager.

        Args:
            agent: instance to manage
            session: Optional session ID or query to load and continue conversation
            resources: Optional paths to load as context
        """
        self._agent = agent
        self._current_history: list[ModelMessage] = []
        self._last_messages: list[ModelMessage] = []
        self._pending_messages: deque[ModelRequest] = deque()
        self._resources = list(resources)  # Store for async loading
        # Generate new ID if none provided
        self.id = str(uuid4())

        if session is not None:
            storage = self._agent.context.storage
            match session:
                case SessionQuery():
                    messages = storage.filter_messages_sync(session)
                    self._current_history = [to_model_message(msg) for msg in messages]
                    if session.name:
                        self.id = session.name
                case _:  # SessionIdType
                    self.id = str(session)
                    query = SessionQuery(name=self.id)
                    messages = storage.filter_messages_sync(query)
                    self._current_history = [to_model_message(msg) for msg in messages]

    def get_initialization_tasks(self) -> list[Coroutine[Any, Any, Any]]:
        """Get all initialization coroutines."""
        self._resources = []  # Clear so we dont load again on async init
        return [self.load_context_source(source) for source in self._resources]

    async def __aenter__(self) -> Self:
        """Initialize when used standalone."""
        tasks = self.get_initialization_tasks()
        if tasks:
            await asyncio.gather(*tasks)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Clean up any pending messages."""
        self._pending_messages.clear()

    def __bool__(self) -> bool:
        return bool(self._pending_messages) or bool(self._current_history)

    def __repr__(self) -> str:
        return f"ConversationManager(id={self.id!r})"

    def __prompt__(self) -> str:
        if not self._current_history:
            return "No conversation history"

        last_msgs = self._current_history[-2:]
        parts = ["Recent conversation:"]
        parts.extend(
            f"{get_message_role(msg).title()}: {format_part(part)[:100]}..."
            for msg in last_msgs
            for part in msg.parts
        )
        return "\n".join(parts)

    @overload
    def __getitem__(self, key: int) -> ChatMessage[Any]: ...

    @overload
    def __getitem__(self, key: slice | str) -> list[ChatMessage[Any]]: ...

    def __getitem__(
        self, key: int | slice | str
    ) -> ChatMessage[Any] | list[ChatMessage[Any]]:
        """Access conversation history.

        Args:
            key: Either:
                - Integer index for single message
                - Slice for message range
                - Agent name for conversation history with that agent
        """
        match key:
            case int():
                return convert_model_message(self._current_history[key])
            case slice():
                return [convert_model_message(msg) for msg in self._current_history[key]]
            case str():
                query = SessionQuery(name=key)
                return self._agent.context.storage.filter_messages_sync(query=query)

    def __contains__(self, item: Any) -> bool:
        """Check if item is in history."""
        return item in self._current_history

    def __len__(self) -> int:
        """Get length of history."""
        return len(self._current_history)

    def get_message_tokens(self, message: ModelMessage) -> int:
        """Get token count for a single message."""
        import tiktoken

        encoding = tiktoken.encoding_for_model(self._agent.model_name or "gpt-3.5-turbo")
        # Format message to text for token counting
        content = "\n".join(format_part(part) for part in message.parts)
        return len(encoding.encode(content))

    async def format_history(
        self,
        *,
        max_tokens: int | None = None,
        include_system: bool = False,
        format_template: str | None = None,
        num_messages: int | None = None,  # Add this parameter
    ) -> str:
        """Format conversation history as a single context message.

        Args:
            max_tokens: Optional limit to include only last N tokens
            include_system: Whether to include system messages
            format_template: Optional custom format (defaults to agent/message pairs)
            num_messages: Optional limit to include only last N messages
        """
        template = format_template or "Agent {agent}: {content}\n"
        messages: list[str] = []
        token_count = 0

        # Get messages, optionally limited
        history = self._current_history
        if num_messages:
            history = history[-num_messages:]

        if max_tokens:
            history = list(reversed(history))  # Start from newest when token limited

        for msg in history:
            # Check message type instead of role string
            if not include_system and isinstance(msg, SystemPromptPart):
                continue
            content = "\n".join(format_part(part) for part in msg.parts)
            formatted = template.format(agent=get_message_role(msg), content=content)

            if max_tokens:
                # Count tokens in this message
                msg_tokens = self.get_message_tokens(msg)
                if token_count + msg_tokens > max_tokens:
                    break
                token_count += msg_tokens
                # Add to front since we're going backwards
                messages.insert(0, formatted)
            else:
                messages.append(formatted)

        return "\n".join(messages)

    async def load_context_source(self, source: Resource | PromptType | str):
        """Load context from a single source."""
        try:
            match source:
                case str():
                    await self.add_context_from_path(source)
                case BaseResource():
                    await self.add_context_from_resource(source)
                case BasePrompt():
                    await self.add_context_from_prompt(source)
        except Exception:
            msg = "Failed to load context from %s"
            logger.exception(msg, "file" if isinstance(source, str) else source.type)

    def load_history_from_database(
        self,
        session: SessionIdType | SessionQuery = None,
        *,
        since: datetime | None = None,
        until: datetime | None = None,
        roles: set[MessageRole] | None = None,
        limit: int | None = None,
    ):
        """Load conversation history from database.

        Args:
            session: Session ID or query config
            since: Only include messages after this time (override)
            until: Only include messages before this time (override)
            roles: Only include messages with these roles (override)
            limit: Maximum number of messages to return (override)
        """
        storage = self._agent.context.storage
        match session:
            case SessionQuery() as query:
                # Override query params if provided
                if since is not None or until is not None or roles or limit:
                    update = {
                        "since": since.isoformat() if since else None,
                        "until": until.isoformat() if until else None,
                        "roles": roles,
                        "limit": limit,
                    }
                    query = query.model_copy(update=update)
                messages = storage.filter_messages_sync(query)
                self._current_history = [to_model_message(msg) for msg in messages]
                if query.name:
                    self.id = query.name
            case str() | UUID():
                self.id = str(session)
                query = SessionQuery(
                    name=self.id,
                    since=since.isoformat() if since else None,
                    until=until.isoformat() if until else None,
                    roles=roles,
                    limit=limit,
                )
                messages = storage.filter_messages_sync(query)
                self._current_history = [to_model_message(msg) for msg in messages]
            case None:
                # Use current session ID
                query = SessionQuery(
                    name=self.id,
                    since=since.isoformat() if since else None,
                    until=until.isoformat() if until else None,
                    roles=roles,
                    limit=limit,
                )
                messages = storage.filter_messages_sync(query)
                self._current_history = [to_model_message(msg) for msg in messages]

    def get_history(
        self,
        include_pending: bool = True,
        roles: set[type[ModelMessage]] | None = None,
    ) -> list[ModelMessage]:
        """Get current conversation history.

        Args:
            include_pending: Whether to include pending messages in the history.
                             If True, pending messages are moved to main history.
            roles: Message roles to include

        Returns:
            List of messages in chronological order
        """
        if include_pending and self._pending_messages:
            self._current_history.extend(self._pending_messages)
            self._pending_messages.clear()

        if roles:
            return [
                msg
                for msg in self._current_history
                if any(isinstance(msg, r) for r in roles)
            ]
        return self._current_history

    def get_pending_messages(self) -> list[ModelMessage]:
        """Get messages that will be included in next interaction."""
        return list(self._pending_messages)

    def clear_pending(self):
        """Clear pending messages without adding them to history."""
        self._pending_messages.clear()

    def set_history(self, history: list[ModelMessage]):
        """Update conversation history after run."""
        self._current_history = history

    def clear(self):
        """Clear conversation history and prompts."""
        self._current_history = []
        self._last_messages = []
        event = self.HistoryCleared(session_id=str(self.id))
        self.history_cleared.emit(event)

    @asynccontextmanager
    async def temporary_state(
        self,
        history: list[AnyPromptType] | SessionQuery | None = None,
        *,
        replace_history: bool = False,
    ) -> AsyncIterator[Self]:
        """Temporarily set conversation history.

        Args:
            history: Optional list of prompts to use as temporary history.
                    Can be strings, BasePrompts, or other prompt types.
            replace_history: If True, only use provided history. If False, append
                    to existing history.
        """
        old_history = self._current_history.copy()

        try:
            messages: list[ChatMessage[Any]] = []
            if history is not None:
                if isinstance(history, SessionQuery):
                    # Get ChatMessages and convert to ModelMessages
                    messages = await self._agent.context.storage.filter_messages(history)
                else:
                    # Convert prompts to ModelMessages
                    messages = [
                        ChatMessage(content=await to_prompt(p), role="user")
                        for p in history
                    ]

            model_messages = [to_model_message(msg) for msg in messages]

            if replace_history:
                self._current_history = model_messages
            else:
                self._current_history.extend(model_messages)

            yield self

        finally:
            self._current_history = old_history

    @property
    def last_run_messages(self) -> list[ChatMessage]:
        """Get messages from the last run converted to our format."""
        return [convert_model_message(msg) for msg in self._last_messages]

    def add_context_message(
        self,
        content: str,
        source: str | None = None,
        **metadata: Any,
    ):
        """Add a context message.

        Args:
            content: Text content to add
            source: Description of content source
            **metadata: Additional metadata to include with the message
        """
        meta_str = ""
        if metadata:
            meta_str = "\n".join(f"{k}: {v}" for k, v in metadata.items())
            meta_str = f"\nMetadata:\n{meta_str}\n"

        header = f"Content from {source}:" if source else "Additional context:"
        formatted = f"{header}{meta_str}\n{content}\n"
        message = ModelRequest(parts=[UserPromptPart(content=formatted)])
        self._pending_messages.append(message)
        # Emit as user message - will trigger logging through existing flow

        chat_message = ChatMessage[str](
            content=formatted,
            role="user",
            name="user",
            model=self._agent.model_name,
            metadata=metadata,
        )
        self._agent.message_received.emit(chat_message)

    async def add_context_from_path(
        self,
        path: StrPath,
        *,
        convert_to_md: bool = False,
        **metadata: Any,
    ):
        """Add file or URL content as context message.

        Args:
            path: Any UPath-supported path
            convert_to_md: Whether to convert content to markdown
            **metadata: Additional metadata to include with the message

        Raises:
            ValueError: If content cannot be loaded or converted
        """
        path_obj = UPath(path)

        if convert_to_md:
            try:
                from markitdown import MarkItDown

                md = MarkItDown()

                # Direct handling for local paths and http(s) URLs
                if path_obj.protocol in ("", "file", "http", "https"):
                    result = md.convert(path_obj.path)
                else:
                    with tempfile.NamedTemporaryFile(suffix=path_obj.suffix) as tmp:
                        tmp.write(path_obj.read_bytes())
                        tmp.flush()
                        result = md.convert(tmp.name)

                content = result.text_content
                source = f"markdown:{path_obj.name}"

            except Exception as e:
                msg = f"Failed to convert {path_obj} to markdown: {e}"
                raise ValueError(msg) from e
        else:
            try:
                content = path_obj.read_text()
                source = f"{path_obj.protocol}:{path_obj.name}"
            except Exception as e:
                msg = f"Failed to read {path_obj}: {e}"
                raise ValueError(msg) from e

        self.add_context_message(content, source=source, **metadata)

    async def add_context_from_resource(self, resource: Resource | str):
        """Add content from a LLMling resource."""
        if not self._agent.runtime:
            msg = "No runtime available"
            raise RuntimeError(msg)

        if isinstance(resource, str):
            content = await self._agent.runtime.load_resource(resource)
            self.add_context_message(
                str(content.content),
                source=f"Resource {resource}",
                mime_type=content.metadata.mime_type,
                **content.metadata.extra,
            )
        else:
            loader = self._agent.runtime._loader_registry.get_loader(resource)
            async for content in loader.load(resource):
                self.add_context_message(
                    str(content.content),
                    source=f"{resource.type}:{resource.uri}",
                    mime_type=content.metadata.mime_type,
                    **content.metadata.extra,
                )

    async def add_context_from_prompt(
        self,
        prompt: PromptType,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ):
        """Add rendered prompt content as context message.

        Args:
            prompt: LLMling prompt (static, dynamic, or file-based)
            metadata: Additional metadata to include with the message
            kwargs: Optional kwargs for prompt formatting
        """
        try:
            # Format the prompt using LLMling's prompt system
            messages = await prompt.format(kwargs)
            # Extract text content from all messages
            content = "\n\n".join(msg.get_text_content() for msg in messages)

            self.add_context_message(
                content,
                source=f"prompt:{prompt.name or prompt.type}",
                prompt_args=kwargs,
                **(metadata or {}),
            )
        except Exception as e:
            msg = f"Failed to format prompt: {e}"
            raise ValueError(msg) from e

    def get_history_tokens(self) -> int:
        """Get token count for current history."""
        import tiktoken

        encoding = tiktoken.encoding_for_model(self._agent.model_name or "gpt-3.5-turbo")
        return sum(
            len(encoding.encode(format_part(part)))
            for msg in self._current_history
            for part in msg.parts
        )

    def get_pending_tokens(self) -> int:
        """Get token count for pending messages."""
        import tiktoken

        encoding = tiktoken.encoding_for_model(self._agent.model_name or "gpt-3.5-turbo")
        return sum(
            len(encoding.encode(format_part(part)))
            for msg in self._pending_messages
            for part in msg.parts
        )


if __name__ == "__main__":
    from llmling_agent import Agent

    async def main():
        async with Agent[Any].open() as agent:
            convo = ConversationManager(agent, session="test")
            await convo.add_context_from_path("E:/mcp_zed.yml")
            print(convo._current_history)

    import asyncio

    asyncio.run(main())
