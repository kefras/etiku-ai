
"""Persistent, user-isolated conversation storage for ETIKU AI."""

from datetime import datetime, timezone
from uuid import UUID

from src.etiku_ai.auth import get_current_user, get_supabase


def _authenticated_client():
    """Require an authenticated user for database operations."""
    client = get_supabase()
    user = get_current_user()

    if user is None:
        raise PermissionError("Please sign in to access conversations.")

    return client, str(user.id)


def _validate_uuid(value):
    """Validate conversation IDs before database queries."""
    return str(UUID(str(value)))


def initialize():
    """Retained for compatibility with ETIKU AI."""
    _authenticated_client()


def list_conversations():
    client, user_id = _authenticated_client()

    result = (
        client.table("conversations")
        .select("id,title,created_at,updated_at")
        .eq("user_id", user_id)
        .order("updated_at", desc=True)
        .execute()
    )

    return result.data or []


def create_conversation():
    client, user_id = _authenticated_client()

    result = (
        client.table("conversations")
        .insert({
            "user_id": user_id,
            "title": "New conversation",
        })
        .execute()
    )

    if not result.data:
        raise RuntimeError("Could not create conversation.")

    return result.data[0]["id"]


def get_messages(conversation_id):
    if not conversation_id:
        return []

    client, user_id = _authenticated_client()
    conversation_id = _validate_uuid(conversation_id)

    result = (
        client.table("messages")
        .select("id,role,content,created_at")
        .eq("conversation_id", conversation_id)
        .eq("user_id", user_id)
        .order("created_at")
        .order("id")
        .execute()
    )

    return result.data or []


def add_message(conversation_id, role, content):
    client, user_id = _authenticated_client()
    conversation_id = _validate_uuid(conversation_id)

    if role not in ("user", "assistant"):
        raise ValueError("Invalid message role.")

    if not isinstance(content, str) or not content.strip():
        raise ValueError("Message content cannot be empty.")

    # Save the message.
    result = (
        client.table("messages")
        .insert({
            "conversation_id": conversation_id,
            "user_id": user_id,
            "role": role,
            "content": content,
        })
        .execute()
    )

    if not result.data:
        raise RuntimeError("Could not save message.")

    # Update conversation activity timestamp.
    now = datetime.now(timezone.utc).isoformat()

    (
        client.table("conversations")
        .update({"updated_at": now})
        .eq("id", conversation_id)
        .eq("user_id", user_id)
        .execute()
    )

    return result.data[0]


def rename_conversation(conversation_id, title):
    client, user_id = _authenticated_client()
    conversation_id = _validate_uuid(conversation_id)

    title = title.strip()

    if not title:
        raise ValueError("Conversation title cannot be empty.")

    (
        client.table("conversations")
        .update({"title": title[:150]})
        .eq("id", conversation_id)
        .eq("user_id", user_id)
        .execute()
    )


def delete_conversation(conversation_id):
    client, user_id = _authenticated_client()
    conversation_id = _validate_uuid(conversation_id)

    (
        client.table("conversations")
        .delete()
        .eq("id", conversation_id)
        .eq("user_id", user_id)
        .execute()
    )
