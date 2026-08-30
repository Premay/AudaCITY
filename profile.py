from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.dependencies import get_access_token, get_auth_service
from app.schemas.auth import ProfileUpdateRequest
from app.services.auth.supabase import SupabaseAuthService

router = APIRouter(prefix="/profile", tags=["profile"])


async def authenticated_user_id(service: SupabaseAuthService, access_token: str) -> str:
    user = await service.get_user(access_token)
    user_id = user.get("id")
    if not isinstance(user_id, str):
        from fastapi import HTTPException

        raise HTTPException(status_code=401, detail="Authentication is required.")
    return user_id


@router.get("")
async def get_profile(
    access_token: Annotated[str, Depends(get_access_token)],
    service: Annotated[SupabaseAuthService, Depends(get_auth_service)],
) -> dict[str, Any]:
    user_id = await authenticated_user_id(service, access_token)
    return await service.get_profile(access_token, user_id)


@router.patch("")
async def update_profile(
    request: ProfileUpdateRequest,
    access_token: Annotated[str, Depends(get_access_token)],
    service: Annotated[SupabaseAuthService, Depends(get_auth_service)],
) -> dict[str, Any]:
    changes = request.model_dump(exclude_none=True, mode="json")
    if not changes:
        from fastapi import HTTPException

        raise HTTPException(status_code=400, detail="Provide at least one profile field to update.")
    user_id = await authenticated_user_id(service, access_token)
    return await service.update_profile(access_token, user_id, changes)
