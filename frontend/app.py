"""
app.py -- Streamlit Frontend for the Counter App

This is a separate microservice. It does NOT talk to the database directly.
It talks to the FastAPI backend via HTTP requests.

    [Streamlit]  -- HTTP -->  [FastAPI]  -- SQL -->  [PostgreSQL]

This separation is the microservices pattern:
- Frontend only knows "call this URL to get/change the count"
- Frontend has no idea PostgreSQL exists
- You could swap PostgreSQL for MySQL and the frontend wouldn't change
"""

import streamlit as st
import requests
import os

# The URL where the FastAPI backend is running
# Default: localhost:8000 (when running locally)
# In Docker/K8s: this will point to the container/service name
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Counter App", layout="centered")

st.title("Counter App")
st.caption("A simple counter to learn Docker, Kubernetes, and Monitoring")

st.divider()


def get_count():
    """Call GET /counter on the FastAPI backend."""
    try:
        response = requests.get(f"{API_URL}/counter", timeout=5)
        response.raise_for_status()
        return response.json()["value"]
    except requests.exceptions.ConnectionError:
        st.error(
            f"Cannot connect to the API at {API_URL}. "
            "Is the FastAPI backend running?"
        )
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None


def call_action(action):
    """Call POST /counter/<action> on the FastAPI backend."""
    try:
        response = requests.post(f"{API_URL}/counter/{action}", timeout=5)
        response.raise_for_status()
        return response.json()["value"]
    except Exception as e:
        st.error(f"Error: {e}")
        return None


# Display the current count
count = get_count()

if count is not None:
    # Big number display
    st.markdown(
        f"<h1 style='text-align: center; font-size: 120px;'>{count}</h1>",
        unsafe_allow_html=True,
    )

    # Buttons in a row
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("- 1", use_container_width=True):
            call_action("decrement")
            st.rerun()

    with col2:
        if st.button("Reset", use_container_width=True):
            call_action("reset")
            st.rerun()

    with col3:
        if st.button("+ 1", use_container_width=True):
            call_action("increment")
            st.rerun()

    st.divider()

    # Show connection info (helpful for debugging in Docker/K8s later)
    with st.expander("Connection Info"):
        st.text(f"API URL: {API_URL}")

        # Check API health
        try:
            health = requests.get(f"{API_URL}/health", timeout=5)
            st.text(f"API Health: {health.json()['status']}")
        except Exception:
            st.text("API Health: unreachable")
