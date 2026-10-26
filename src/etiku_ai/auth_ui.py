
"""Login and registration interface for ETIKU AI."""

import logging

import streamlit as st

from src.etiku_ai.auth import (
    get_current_user,
    sign_in,
    sign_up,
)

logger = logging.getLogger(__name__)


def render_auth():
    """Display authentication forms and return the signed-in user."""

    user = get_current_user()

    if user:
        return user

    st.title("ETIKU AI")
    st.caption("Intelligence. Knowledge. Action.")

    st.subheader("Welcome to ETIKU AI")

    st.write(
        "Sign in to continue your conversations "
        "or create an account to get started."
    )

    login_tab, signup_tab = st.tabs(
        ["Sign in", "Create account"]
    )

    # ---------------------------------------------
    # SIGN IN
    # ---------------------------------------------

    with login_tab:
        with st.form("login_form"):

            email = st.text_input(
                "Email",
                key="login_email",
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_password",
            )

            submitted = st.form_submit_button(
                "Sign in",
                use_container_width=True,
            )

            if submitted:

                if not email.strip() or not password:
                    st.warning(
                        "Please enter your email and password."
                    )

                else:
                    try:
                        response = sign_in(
                            email.strip(),
                            password,
                        )

                        if response.user and response.session:
                            st.success("Signed in successfully.")
                            st.rerun()
                        else:
                            st.error(
                                "Unable to complete sign in."
                            )

                    except Exception as exc:
                        error_type = type(exc).__name__

                        print(
                            "ETIKU AI signup error type:",
                            error_type,
                        )

                        st.error(
                            "Registration failed. "
                            "Check the VS Code terminal "
                            "for details."
                        )

    # ---------------------------------------------
    # CREATE ACCOUNT
    # ---------------------------------------------

    with signup_tab:
        with st.form("signup_form"):

            email = st.text_input(
                "Email address",
                key="signup_email",
            )

            password = st.text_input(
                "Create password",
                type="password",
                key="signup_password",
            )

            confirm_password = st.text_input(
                "Confirm password",
                type="password",
                key="signup_confirm_password",
            )

            submitted = st.form_submit_button(
                "Create account",
                use_container_width=True,
            )

            if submitted:

                if not email.strip() or not password:
                    st.warning(
                        "Please complete all required fields."
                    )

                elif len(password) < 8:
                    st.warning(
                        "Password must contain at least "
                        "8 characters."
                    )

                elif password != confirm_password:
                    st.error(
                        "Passwords do not match."
                    )

                else:
                    try:
                        response = sign_up(
                            email.strip(),
                            password,
                        )

                        if response.session and response.user:
                            st.success(
                                "Account created successfully."
                            )
                            st.rerun()

                        else:
                            st.success(
                                "If registration is accepted, "
                                "check your email for a "
                                "confirmation link before signing in."
                            )

                    except Exception as exc:
                        error_type = type(exc).__name__

                        # Show diagnostic details only in the
                        # local server terminal.
                        logger.error(
                            "ETIKU AI signup error type: %s",
                            error_type,
                        )

                        # Avoid logging passwords, tokens,
                        # or complete authentication responses.
                        st.error(
                            "Registration failed. "
                            "Check your Supabase authentication "
                            "settings and the VS Code terminal."
                        )

    # Stop the chatbot from loading until authenticated.
    st.stop()
