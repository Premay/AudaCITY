from fastapi import APIRouter

router = APIRouter(tags=["system"])


@router.get("/health", summary="Check whether the API is running")
def health_check() -> dict[str, str]:
    """A dependency-free endpoint suitable for deployment health checks."""
    return {"status": "ok"}
