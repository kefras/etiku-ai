import streamlit as st

def render_settings():
    with st.sidebar.expander("⚙️ Settings"):
        st.selectbox(
            "Response style",
            ["Balanced", "Detailed", "Concise"],
            key="response_style",
        )

        st.selectbox(
            "Creativity",
            ["Balanced", "Creative", "Precise"],
            key="creativity",
        )

        st.toggle(
            "Show conversation history",
            value=True,
            key="show_history",
        )