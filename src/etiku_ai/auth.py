
"""Supabase authentication for ETIKU AI."""

import os

import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()


def get_config(name):
    value = os.getenv(name)
    if value:
        return value

    try:
        return st.secrets.get(name)
    except (FileNotFoundError, KeyError):
        return None


def get_supabase():
    """Return a Supabase client for the current Streamlit session."""

    url = get_config("SUPABASE_URL")
    key = get_config("SUPABASE_KEY")

    if not url or not key:
        raise RuntimeError(
            "Missing SUPABASE_URL or SUPABASE_KEY."
        )

    # Remove any incorrectly added API endpoint.
    url = url.strip().rstrip("/")

    for suffix in ("/rest/v1", "/auth/v1"):
        if url.endswith(suffix):
            url = url[: -len(suffix)]

    if "_supabase_client" not in st.session_state:
        st.session_state["_supabase_client"] = create_client(
            url,
            key,
        )

    return st.session_state["_supabase_client"]


def get_current_user():
    """Retrieve the signed-in user, if the session is valid."""

    client = get_supabase()

    try:
        response = client.auth.get_user()
        return response.user
    except Exception:
        return None


def sign_up(email, password):
    """Register a new ETIKU AI user."""

    client = get_supabase()

    return client.auth.sign_up({
        "email": email,
        "password": password,
    })


def sign_in(email, password):
    """Sign in an existing ETIKU AI user."""

    client = get_supabase()

    return client.auth.sign_in_with_password({
        "email": email,
        "password": password,
    })



def sign_out():
    """Sign out and clear session-specific authentication state."""

    client = get_supabase()

    try:
        client.auth.sign_out()
    finally:
        st.session_state.pop("_supabase_client", None)
        st.session_state.pop("conversation_id", None)

        # Remove any temporary chat data retained in the session.
        st.session_state.pop("_etiku_conversations", None)
