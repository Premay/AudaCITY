"""FastAPI application entry point for EduPrep."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title="EduPrep API",
    version="0.1.0",
    description="Backend API for the EduPrep mobile application.",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Keep validation failures useful without exposing internal implementation details."""
    return JSONResponse(
        status_code=422,
        content={"error": "Invalid request.", "details": exc.errors()},
    )


app.include_router(api_router, prefix=settings.api_v1_prefix)
