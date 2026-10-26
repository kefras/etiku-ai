
"""ETIKU AI v2.4 - Gemini chatbot with session-isolated chat history."""

import os
from collections import OrderedDict
from datetime import date, datetime
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from src.etiku_ai.auth import sign_out
from src.etiku_ai.auth_ui import render_auth

from src.etiku_ai.assistant import stream_response
from src.etiku_ai.settings import render_settings
from src.etiku_ai.supabase_storage import (
    add_message,
    create_conversation,
    delete_conversation,
    get_messages,
    initialize,
    list_conversations,
    rename_conversation,
)


# --------------------------------------------------
# APPLICATION CONFIGURATION
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

st.set_page_config(
    page_title="ETIKU AI | Intelligence. Knowledge. Action.",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

css_file = ROOT / "assets" / "style.css"

if css_file.exists():
    st.markdown(
        f"<style>{css_file.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )

# Require login before accessing conversations
user = render_auth()

# Initialize authenticated database storage
initialize()

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None


# --------------------------------------------------
# CONVERSATION DATE HELPERS
# --------------------------------------------------

def parse_chat_timestamp(value):
    """Convert stored timestamps to local datetime."""

    if value is None or value == "":
        return None

    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, (int, float)):
        try:
            parsed = datetime.fromtimestamp(value)
        except (ValueError, OverflowError, OSError):
            return None
    else:
        try:
            parsed = datetime.fromisoformat(
                str(value).replace("Z", "+00:00")
            )
        except (ValueError, TypeError):
            return None

    if parsed.tzinfo is not None:
        parsed = parsed.astimezone()

    return parsed


def group_conversations(chats):
    """Organize conversations by date."""

    today = datetime.now().astimezone().date()

    labels = (
        "Today",
        "Yesterday",
        "Previous 7 Days",
        "Previous 30 Days",
        "Older",
    )

    groups = OrderedDict(
        (label, []) for label in labels
    )

    for chat in chats:
        timestamp = parse_chat_timestamp(
            chat.get("updated_at") or chat.get("created_at")
        )

        if timestamp is None:
            group = "Older"
        else:
            age = (today - timestamp.date()).days

            if age <= 0:
                group = "Today"
            elif age == 1:
                group = "Yesterday"
            elif age <= 7:
                group = "Previous 7 Days"
            elif age <= 30:
                group = "Previous 30 Days"
            else:
                group = "Older"

        groups[group].append(chat)

    return {
        label: items
        for label, items in groups.items()
        if items
    }


def get_gemini_api_key():
    """Read Gemini credentials locally or from Streamlit Cloud."""

    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        return api_key

    try:
        return st.secrets.get("GEMINI_API_KEY")
    except (FileNotFoundError, KeyError):
        return None


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("🧠 ETIKU AI")
    st.caption("Intelligence. Knowledge. Action.")

    if st.button(
        "New chat",
        use_container_width=True,
        type="primary",
    ):
        st.session_state.conversation_id = None
        st.rerun()

    search_query = st.text_input(
        "Search chats",
        placeholder="Search conversations...",
        key="conversation_search",
    )

    st.divider()

    if st.session_state.get("show_history", True):

        all_chats = list_conversations()
        query = search_query.strip().casefold()

        if query:
            chats = [
                chat
                for chat in all_chats
                if query in str(chat["title"]).casefold()
            ]
        else:
            chats = all_chats

        if not chats:
            st.caption(
                "No matching conversations found."
                if query
                else "No conversations yet."
            )

        grouped_chats = group_conversations(chats)

        for group_name, group_chats in grouped_chats.items():

            st.caption(group_name.upper())

            for chat in group_chats:

                chat_id = str(chat["id"])
                title = str(chat["title"])

                selected = (
                    chat_id
                    == str(st.session_state.conversation_id)
                )

                col_chat, col_menu = st.columns(
                    [5, 1],
                    gap="small",
                )

                with col_chat:
                    if st.button(
                        title,
                        key=f"open_{chat_id}",
                        use_container_width=True,
                        type="primary" if selected else "secondary",
                        help=title,
                    ):
                        st.session_state.conversation_id = chat["id"]
                        st.rerun()

                with col_menu:
                    with st.popover("..."):

                        st.caption("Manage conversation")

                        new_title = st.text_input(
                            "Conversation name",
                            value=title,
                            key=f"rename_{chat_id}",
                        )

                        if st.button(
                            "Save name",
                            key=f"save_{chat_id}",
                            use_container_width=True,
                        ):
                            if new_title.strip():
                                rename_conversation(
                                    chat["id"],
                                    new_title.strip(),
                                )
                                st.rerun()

                        if st.button(
                            "Delete conversation",
                            key=f"delete_{chat_id}",
                            use_container_width=True,
                        ):
                            delete_conversation(chat["id"])

                            if selected:
                                st.session_state.conversation_id = None

                            st.rerun()

    else:
        st.caption("Conversation history is hidden.")

    st.divider()

    # Render settings exactly once.
    render_settings()

    st.divider()

    st.caption("ETIKU AI | Version 2.4")
    st.caption(
        "Conversations are temporary and isolated by session."
    )

    st.caption(f"Signed in as: {user.email}")

    if st.button("Sign out", use_container_width=True):
        sign_out()
        st.rerun()

    st.divider()

# --------------------------------------------------
# MAIN CHAT INTERFACE
# --------------------------------------------------

conversation_id = st.session_state.conversation_id

messages = (
    get_messages(conversation_id)
    if conversation_id
    else []
)

if not messages:
    st.markdown(
        """
        <div class="etiku-hero">
            <span class="etiku-mark">ETIKU</span>
            <h1>What can we explore today?</h1>
            <p>
                Your intelligent companion for ideas,
                code, research and problem-solving.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# DISPLAY SAVED MESSAGES
# --------------------------------------------------

for message in messages:

    role = message["role"]
    avatar = "🧠" if role == "assistant" else "👤"

    with st.chat_message(role, avatar=avatar):
        st.markdown(message["content"])


# --------------------------------------------------
# USER INPUT AND GEMINI RESPONSE
# --------------------------------------------------

prompt = st.chat_input("Message ETIKU AI...")

if prompt:

    if not conversation_id:
        conversation_id = create_conversation()
        st.session_state.conversation_id = conversation_id

    if not messages:
        conversation_title = (
            prompt.replace("\n", " ").strip()[:55]
        )

        rename_conversation(
            conversation_id,
            conversation_title or "New conversation",
        )

    add_message(
        conversation_id,
        "user",
        prompt,
    )

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🧠"):

        api_key = get_gemini_api_key()

        if not api_key:
            st.error(
                "Missing GEMINI_API_KEY. "
                "Configure it in your .env file locally "
                "or Streamlit Cloud Secrets."
            )
        else:
            try:
                history = get_messages(conversation_id)[-24:]

                answer = st.write_stream(
                    stream_response(
                        history,
                        api_key,
                        response_style=st.session_state.get(
                            "response_style", "Balanced"
                        ),
                        creativity=st.session_state.get(
                            "creativity", "Balanced"
                        ),
                    )
                )

                if isinstance(answer, str) and answer.strip():
                    add_message(
                        conversation_id,
                        "assistant",
                        answer,
                    )
                else:
                    st.warning(
                        "The model returned an empty response."
                    )

            except Exception as exc:
                st.error(
                    "Unable to generate a response "
                    f"({type(exc).__name__}). "
                    "Please try again."
                )

                print(
                    "ETIKU AI generation error: "
                    f"{type(exc).__name__}: {exc}"
                )

    st.rerun()
