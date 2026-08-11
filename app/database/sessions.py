"""
Temporary chat session store.

Provides in-memory server-side persistence of chat conversation
history, keyed by session ID and scoped to the owning user.

Like ``app.database.users``, this is a development-oriented, single
-process store. It does not survive a restart and does not work
across multiple application instances. A production deployment should
replace this with a real store (e.g. Azure Cosmos DB, Redis, or a
relational database) behind the same functions.
"""

from __future__ import annotations

import threading
import time
import uuid

from app.core.config import settings
from app.models.chat import ChatMessage


class ChatSession:
    """A stored chat conversation, owned by a single user."""

    def __init__(
        self,
        session_id: str,
        owner: str,
    ) -> None:
        """
        Initialize a new, empty chat session.

        Args:
            session_id: Unique session identifier.
            owner: Username of the session's owner.
        """

        self.session_id = session_id
        self.owner = owner
        self.messages: list[ChatMessage] = []
        self.created_at = time.time()
        self.updated_at = self.created_at


_sessions: dict[str, ChatSession] = {}
_lock = threading.Lock()


def create_session(
    owner: str,
) -> ChatSession:
    """
    Create and store a new, empty chat session for a user.

    If the user already has ``settings.session_max_per_user`` sessions,
    the oldest (by last update) is evicted to bound memory use.

    Args:
        owner: Username of the session's owner.

    Returns:
        The newly created session.
    """

    with _lock:
        owned = sorted(
            (s for s in _sessions.values() if s.owner == owner),
            key=lambda s: s.updated_at,
        )

        while len(owned) >= settings.session_max_per_user:
            oldest = owned.pop(0)
            _sessions.pop(oldest.session_id, None)

        session = ChatSession(
            session_id=str(uuid.uuid4()),
            owner=owner,
        )

        _sessions[session.session_id] = session

        return session


def get_session(
    session_id: str,
    owner: str,
) -> ChatSession | None:
    """
    Retrieve a session by ID, scoped to its owner.

    Args:
        session_id: Session identifier.
        owner: Username expected to own the session.

    Returns:
        The session if it exists and belongs to ``owner``, else
        ``None``. A session that exists but belongs to a different
        user is treated as not found, so ownership never leaks
        through error messages.
    """

    with _lock:
        session = _sessions.get(session_id)

        if session is None or session.owner != owner:
            return None

        return session


def list_sessions(
    owner: str,
) -> list[ChatSession]:
    """
    List all sessions owned by a user, most recently updated first.

    Args:
        owner: Username to list sessions for.

    Returns:
        Owned sessions, most recently updated first.
    """

    with _lock:
        owned = [s for s in _sessions.values() if s.owner == owner]

        return sorted(owned, key=lambda s: s.updated_at, reverse=True)


def append_turn(
    session: ChatSession,
    user_message: ChatMessage,
    assistant_message: ChatMessage,
) -> None:
    """
    Append a user/assistant turn to a session and persist it.

    History is capped to the most recent ``settings.session_max_messages``
    messages so a long-running conversation cannot grow the stored
    context (and therefore the tokens sent to Azure OpenAI on every
    subsequent turn) without bound.

    Args:
        session: The session to update.
        user_message: The user's message for this turn.
        assistant_message: The assistant's response for this turn.
    """

    with _lock:
        session.messages.append(user_message)
        session.messages.append(assistant_message)

        max_messages = settings.session_max_messages

        if len(session.messages) > max_messages:
            session.messages = session.messages[-max_messages:]

        session.updated_at = time.time()


def delete_session(
    session_id: str,
    owner: str,
) -> bool:
    """
    Delete a session, scoped to its owner.

    Args:
        session_id: Session identifier.
        owner: Username expected to own the session.

    Returns:
        True if a session was deleted, False if no matching session
        was found for that owner.
    """

    with _lock:
        session = _sessions.get(session_id)

        if session is None or session.owner != owner:
            return False

        del _sessions[session_id]

        return True


def clear_all() -> None:
    """
    Remove every stored session.

    Intended for tests, so each test starts from a clean store.
    """

    with _lock:
        _sessions.clear()
