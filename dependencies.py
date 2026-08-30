"""Reusable API dependencies."""

from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import Settings, get_settings
from app.services.catalog import CatalogService
from app.services.auth.supabase import SupabaseAuthService

bearer_scheme = HTTPBearer(auto_error=False)


def get_auth_service(settings: Annotated[Settings, Depends(get_settings)]) -> SupabaseAuthService:
    return SupabaseAuthService(settings)


def get_catalog_service(settings: Annotated[Settings, Depends(get_settings)]) -> CatalogService:
    return CatalogService(settings)


async def get_access_token(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> str:
    if credentials is None:
        from fastapi import HTTPException

        raise HTTPException(status_code=401, detail="Authentication is required.")
    return credentials.credentials
