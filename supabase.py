"""Small server-side client for Supabase Auth and the protected profile record."""

from typing import Any

import httpx
from fastapi import HTTPException, status

from app.config import Settings


class SupabaseAuthService:
    """Keeps Supabase HTTP details out of route handlers and Flutter."""

    def __init__(self, settings: Settings) -> None:
        if not settings.supabase_url or not settings.supabase_anon_key:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication is not configured yet.",
            )
        self.base_url = settings.supabase_url.rstrip("/")
        self.anon_key = settings.supabase_anon_key

    def _headers(self, access_token: str | None = None) -> dict[str, str]:
        headers = {"apikey": self.anon_key, "Content-Type": "application/json"}
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"
        return headers

    async def _request(
        self,
        method: str,
        path: str,
        *,
        payload: dict[str, Any] | None = None,
        access_token: str | None = None,
    ) -> httpx.Response:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                return await client.request(
                    method,
                    f"{self.base_url}{path}",
                    headers=self._headers(access_token),
                    json=payload,
                )
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication service is temporarily unavailable.",
            ) from exc

    async def register(self, payload: dict[str, Any]) -> dict[str, Any]:
        response = await self._request("POST", "/auth/v1/signup", payload=payload)
        if response.is_error:
            raise HTTPException(status_code=400, detail="Registration could not be completed.")
        return response.json()

    async def login(self, email: str, password: str) -> dict[str, Any]:
        response = await self._request(
            "POST",
            "/auth/v1/token?grant_type=password",
            payload={"email": email, "password": password},
        )
        if response.is_error:
            raise HTTPException(status_code=401, detail="Invalid email or password.")
        return response.json()

    async def logout(self, access_token: str) -> None:
        response = await self._request("POST", "/auth/v1/logout", access_token=access_token)
        if response.is_error:
            raise HTTPException(status_code=401, detail="Your session is no longer valid.")

    async def send_password_reset(self, email: str) -> None:
        response = await self._request("POST", "/auth/v1/recover", payload={"email": email})
        if response.is_error:
            raise HTTPException(
                status_code=503,
                detail="Password reset is temporarily unavailable. Please try again.",
            )

    async def get_user(self, access_token: str) -> dict[str, Any]:
        response = await self._request("GET", "/auth/v1/user", access_token=access_token)
        if response.is_error:
            raise HTTPException(status_code=401, detail="Authentication is required.")
        return response.json()

    async def get_profile(self, access_token: str, user_id: str) -> dict[str, Any]:
        response = await self._request(
            "GET",
            f"/rest/v1/profiles?id=eq.{user_id}&select=id,full_name,email,class_level,preferred_exam,created_at,updated_at",
            access_token=access_token,
        )
        if response.is_error:
            raise HTTPException(status_code=503, detail="Profile is temporarily unavailable.")
        records = response.json()
        if not records:
            raise HTTPException(status_code=404, detail="Profile was not found.")
        return records[0]

    async def update_profile(
        self, access_token: str, user_id: str, changes: dict[str, Any]
    ) -> dict[str, Any]:
        response = await self._request(
            "PATCH",
            f"/rest/v1/profiles?id=eq.{user_id}",
            payload=changes,
            access_token=access_token,
        )
        if response.is_error:
            raise HTTPException(status_code=503, detail="Profile could not be updated.")
        return await self.get_profile(access_token, user_id)
