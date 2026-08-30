"""Schemas for FastAPI-mediated Supabase authentication."""

from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class EmailRequest(BaseModel):
    email: str = Field(min_length=3, max_length=254)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().lower()
        if "@" not in normalized or normalized.startswith("@") or normalized.endswith("@"):
            raise ValueError("Enter a valid email address.")
        return normalized


class RegisterRequest(EmailRequest):
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=120)
    class_level: str | None = Field(default=None, max_length=40)


class LoginRequest(EmailRequest):
    password: str = Field(min_length=8, max_length=128)


class ProfileUpdateRequest(BaseModel):
    full_name: str | None = Field(default=None, max_length=120)
    class_level: str | None = Field(default=None, max_length=40)
    preferred_exam: UUID | None = None


class MessageResponse(BaseModel):
    message: str
