"""Application configuration.

On Streamlit Community Cloud, values come from the app's "Secrets" panel
(Settings > Secrets), which populates ``st.secrets``. For local development,
values come from a ``.env`` file via python-dotenv. Never commit a populated
``.env`` file or a populated ``.streamlit/secrets.toml`` file.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import streamlit as st

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


def _get(key: str) -> str | None:
    """Prefer Streamlit secrets, fall back to environment variables."""
    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        # st.secrets raises if no secrets file exists at all (e.g. local dev
        # without .streamlit/secrets.toml) — that's fine, fall back to env.
        pass
    return os.environ.get(key)


@dataclass(frozen=True)
class Settings:
    supabase_url: str | None
    supabase_anon_key: str | None


@st.cache_resource
def get_settings() -> Settings:
    return Settings(
        supabase_url=_get("SUPABASE_URL"),
        supabase_anon_key=_get("SUPABASE_ANON_KEY"),
    )
