
"""Session-isolated conversation storage for ETIKU AI public demo."""

import uuid
from datetime import datetime, timezone

import streamlit as st


def _store():
    if "_etiku_conversations" not in st.session_state:
        st.session_state["_etiku_conversations"] = {}

    return st.session_state["_etiku_conversations"]


def _now():
    return datetime.now(timezone.utc).isoformat()


def initialize():
    _store()


def create_conversation(title="New conversation"):
    conversation_id = str(uuid.uuid4())
    now = _now()

    _store()[conversation_id] = {
        "id": conversation_id,
        "title": title,
        "created_at": now,
        "updated_at": now,
        "messages": [],
    }

    return conversation_id


def list_conversations():
    chats = _store().values()

    return sorted(
        [
            {
                "id": chat["id"],
                "title": chat["title"],
                "created_at": chat["created_at"],
                "updated_at": chat["updated_at"],
            }
            for chat in chats
        ],
        key=lambda chat: chat["updated_at"],
        reverse=True,
    )


def get_messages(conversation_id):
    chat = _store().get(conversation_id)

    if chat is None:
        return []

    return [
        dict(message)
        for message in chat["messages"]
    ]


def add_message(conversation_id, role, content):
    if role not in ("user", "assistant"):
        raise ValueError("Invalid message role")

    chat = _store().get(conversation_id)

    if chat is None:
        raise ValueError("Conversation not found")

    chat["messages"].append(
        {
            "role": role,
            "content": content,
        }
    )

    chat["updated_at"] = _now()


def rename_conversation(conversation_id, title):
    chat = _store().get(conversation_id)

    if chat is None:
        return

    title = title.strip()[:90]

    if title:
        chat["title"] = title


def delete_conversation(conversation_id):
    _store().pop(conversation_id, None)
