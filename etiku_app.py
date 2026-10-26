
"""ETIKU AI v2.3 â€” Gemini chatbot with ChatGPT-style history."""

import os
from collections import OrderedDict
from datetime import date, datetime
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from src.etiku_ai.assistant import stream_response
from src.etiku_ai.settings import render_settings
from src.etiku_ai.session_storage import (
    add_message,
    create_conversation,
    delete_conversation,
    get_messages,
    initialize,
    list_conversations,
    rename_conversation,
)


# ==================================================
# APPLICATION CONFIGURATION
# ==================================================

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

st.set_page_config(
    page_title="ETIKU AI | Intelligence. Knowledge. Action.",
    page_icon="ðŸ§ ",
    layout="wide",
    initial_sidebar_state="expanded",
)

css_file = ROOT / "assets" / "style.css"

if css_file.exists():
    st.markdown(
        f"<style>{css_file.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )

initialize()

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None


# ==================================================
# CONVERSATION DATE HELPERS
# ==================================================

def parse_chat_timestamp(value):
    """Convert a stored timestamp into local datetime."""

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
    """Organize conversations into date-based sections."""

    today = date.today()

    groups = OrderedDict(
        (label, [])
        for label in (
            "Today",
            "Yesterday",
            "Previous 7 Days",
            "Previous 30 Days",
            "Older",
        )
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


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("ðŸ§  ETIKU AI")
    st.caption("Intelligence. Knowledge. Action.")

    # Start a new conversation
    if st.button(
        "âœï¸ New chat",
        use_container_width=True,
        type="primary",
    ):
        st.session_state.conversation_id = None
        st.rerun()

    # Search conversation titles
    search_query = st.text_input(
        "Search chats",
        placeholder="Search conversations...",
        key="conversation_search",
    )

    st.divider()

    # Conversation history
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

                # Open conversation
                with col_chat:

                    if st.button(
                        title,
                        key=f"open_{chat_id}",
                        use_container_width=True,
                        type=(
                            "primary"
                            if selected
                            else "secondary"
                        ),
                        help=title,
                    ):
                        st.session_state.conversation_id = (
                            chat["id"]
                        )
                        st.rerun()

                # Rename or delete conversation
                with col_menu:

                    with st.popover("â‹¯"):

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
                            "ðŸ—‘ï¸ Delete conversation",
                            key=f"delete_{chat_id}",
                            use_container_width=True,
                        ):
                            delete_conversation(chat["id"])

                            if selected:
                                st.session_state.conversation_id = None

                            st.rerun()

    else:
        st.caption("Conversation history is hidden.")

    # Render Settings only once
    st.divider()
    render_settings()

    st.divider()

    st.caption("ETIKU AI Â· Version 2.3")
    st.caption("Your conversations are stored locally.")


# ==================================================
# MAIN CHAT INTERFACE
# ==================================================

conversation_id = st.session_state.conversation_id

messages = (
    get_messages(conversation_id)
    if conversation_id
    else []
)

# Show welcome screen for new chats
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


# ==================================================
# DISPLAY SAVED MESSAGES
# ==================================================

for message in messages:

    role = message["role"]

    avatar = (
        "ðŸ§ "
        if role == "assistant"
        else "ðŸ‘¤"
    )

    with st.chat_message(
        role,
        avatar=avatar,
    ):
        st.markdown(message["content"])


# ==================================================
# USER INPUT AND GEMINI RESPONSE
# ==================================================

prompt = st.chat_input("Message ETIKU AI...")

if prompt:

    # Create conversation on first message
    if not conversation_id:

        conversation_id = create_conversation()
        st.session_state.conversation_id = conversation_id

    # Automatically name new conversations
    if not messages:

        conversation_title = (
            prompt.replace("\n", " ").strip()[:55]
        )

        rename_conversation(
            conversation_id,
            conversation_title or "New conversation",
        )

    # Save user message
    add_message(
        conversation_id,
        "user",
        prompt,
    )

    # Display user message
    with st.chat_message(
        "user",
        avatar="ðŸ‘¤",
    ):
        st.markdown(prompt)


    # Generate Gemini response
    with st.chat_message("assistant", avatar="ðŸ§ "):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            try:
                api_key = st.secrets.get("GEMINI_API_KEY")
            except (FileNotFoundError, KeyError):
                api_key = None

        if not api_key:
            st.error(
                "Missing GEMINI_API_KEY. "
                "Add it to .env locally or Streamlit Cloud Secrets."
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
                    f"Unable to generate response: "
                    f"{type(exc).__name__}"
                )
                print(
                    f"ETIKU AI generation error: {exc}"
                )

    st.rerun()
