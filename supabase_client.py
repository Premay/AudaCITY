"""Synchronous Supabase client for the EduPrep Streamlit app.

This carries over the exact behavior of the original FastAPI service layer
(app/services/auth/supabase.py and app/services/catalog.py from the Phase 0
backend) — same Supabase Auth and PostgREST calls — but is called directly
from Streamlit UI code in-process, instead of being exposed over HTTP for
Flutter to call. There is no HTTP API surface in this app.
"""

from __future__ import annotations

from typing import Any

import httpx
import streamlit as st

from config import Settings, get_settings


class SupabaseError(Exception):
    """Raised for any Supabase Auth/PostgREST failure. Message is user-safe."""


class SupabaseClient:
    def __init__(self, settings: Settings) -> None:
        if not settings.supabase_url or not settings.supabase_anon_key:
            raise SupabaseError(
                "Supabase is not configured yet. Set SUPABASE_URL and "
                "SUPABASE_ANON_KEY in Secrets (Streamlit Cloud) or .env (local)."
            )
        self.base_url = settings.supabase_url.rstrip("/")
        self.anon_key = settings.supabase_anon_key

    def _headers(self, access_token: str | None = None) -> dict[str, str]:
        headers = {"apikey": self.anon_key, "Content-Type": "application/json"}
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"
        return headers

    def _request(
        self,
        method: str,
        path: str,
        *,
        payload: dict[str, Any] | None = None,
        access_token: str | None = None,
    ) -> httpx.Response:
        try:
            with httpx.Client(timeout=10.0) as client:
                return client.request(
                    method,
                    f"{self.base_url}{path}",
                    headers=self._headers(access_token),
                    json=payload,
                )
        except httpx.RequestError as exc:
            raise SupabaseError(
                "The service is temporarily unavailable. Please try again."
            ) from exc

    # --- Auth ---------------------------------------------------------

    def register(
        self,
        email: str,
        password: str,
        full_name: str | None = None,
        class_level: str | None = None,
    ) -> dict[str, Any]:
        metadata = {
            key: value
            for key, value in {"full_name": full_name, "class_level": class_level}.items()
            if value
        }
        response = self._request(
            "POST",
            "/auth/v1/signup",
            payload={"email": email, "password": password, "data": metadata},
        )
        if response.is_error:
            raise SupabaseError("Registration could not be completed. The email may already be in use.")
        return response.json()

    def login(self, email: str, password: str) -> dict[str, Any]:
        response = self._request(
            "POST",
            "/auth/v1/token?grant_type=password",
            payload={"email": email, "password": password},
        )
        if response.is_error:
            raise SupabaseError("Invalid email or password.")
        return response.json()

    def logout(self, access_token: str) -> None:
        response = self._request("POST", "/auth/v1/logout", access_token=access_token)
        if response.is_error:
            raise SupabaseError("Your session is no longer valid.")

    def send_password_reset(self, email: str) -> None:
        response = self._request("POST", "/auth/v1/recover", payload={"email": email})
        if response.is_error:
            raise SupabaseError("Password reset is temporarily unavailable. Please try again.")

    def get_user(self, access_token: str) -> dict[str, Any]:
        response = self._request("GET", "/auth/v1/user", access_token=access_token)
        if response.is_error:
            raise SupabaseError("Your session has expired. Please log in again.")
        return response.json()

    # --- Profile --------------------------------------------------------

    def get_profile(self, access_token: str, user_id: str) -> dict[str, Any]:
        response = self._request(
            "GET",
            f"/rest/v1/profiles?id=eq.{user_id}&select=id,full_name,email,class_level,preferred_exam,created_at,updated_at",
            access_token=access_token,
        )
        if response.is_error:
            raise SupabaseError("Profile is temporarily unavailable.")
        records = response.json()
        if not records:
            raise SupabaseError("Profile was not found.")
        return records[0]

    def update_profile(self, access_token: str, user_id: str, changes: dict[str, Any]) -> dict[str, Any]:
        response = self._request(
            "PATCH",
            f"/rest/v1/profiles?id=eq.{user_id}",
            payload=changes,
            access_token=access_token,
        )
        if response.is_error:
            raise SupabaseError("Profile could not be updated.")
        return self.get_profile(access_token, user_id)

    # --- Catalogue --------------------------------------------------------

    def list_exams(self, access_token: str) -> list[dict[str, Any]]:
        return self._catalog_fetch("exams", "select=id,name,code,description&order=name", access_token)

    def get_exam(self, exam_id: str, access_token: str) -> dict[str, Any]:
        records = self._catalog_fetch(
            "exams", f"id=eq.{exam_id}&select=id,name,code,description", access_token
        )
        if not records:
            raise SupabaseError("Exam was not found.")
        return records[0]

    def list_subjects(self, access_token: str) -> list[dict[str, Any]]:
        return self._catalog_fetch("subjects", "select=id,name,code&order=name", access_token)

    def get_subject(self, subject_id: str, access_token: str) -> dict[str, Any]:
        records = self._catalog_fetch(
            "subjects", f"id=eq.{subject_id}&select=id,name,code", access_token
        )
        if not records:
            raise SupabaseError("Subject was not found.")
        return records[0]

    def list_topics(self, subject_id: str, access_token: str, limit: int = 50) -> list[dict[str, Any]]:
        return self._catalog_fetch(
            "topics",
            f"subject_id=eq.{subject_id}&select=id,subject_id,name,description&order=name&limit={limit}",
            access_token,
        )

    def _catalog_fetch(self, resource: str, query: str, access_token: str) -> list[dict[str, Any]]:
        response = self._request("GET", f"/rest/v1/{resource}?{query}", access_token=access_token)
        if response.status_code in (401, 403):
            raise SupabaseError("Your session has expired. Please log in again.")
        if response.is_error:
            raise SupabaseError("Learning content is temporarily unavailable.")
        return response.json()


def get_client() -> SupabaseClient:
    """Build the Supabase client from current settings (not cached: settings rarely change,
    but constructing a client is cheap and this keeps config edits picked up on rerun)."""
    return SupabaseClient(get_settings())
