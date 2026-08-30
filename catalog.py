"""Read-only access to EduPrep's reference catalogue."""

from typing import Any

import httpx
from fastapi import HTTPException, status

from app.config import Settings


class CatalogService:
    """Fetches seeded exams, subjects, and topics through Supabase RLS."""

    def __init__(self, settings: Settings) -> None:
        if not settings.supabase_url or not settings.supabase_anon_key:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Learning content is not configured yet.",
            )
        self.base_url = settings.supabase_url.rstrip("/")
        self.anon_key = settings.supabase_anon_key

    async def fetch(
        self, resource: str, query: str, access_token: str
    ) -> list[dict[str, Any]]:
        headers = {
            "apikey": self.anon_key,
            "Authorization": f"Bearer {access_token}",
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/rest/v1/{resource}?{query}", headers=headers
                )
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Learning content is temporarily unavailable.",
            ) from exc

        if response.status_code in (401, 403):
            raise HTTPException(status_code=401, detail="Authentication is required.")
        if response.is_error:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Learning content is temporarily unavailable.",
            )
        return response.json()
