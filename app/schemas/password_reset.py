# app/schemas/password_reset.py
from pydantic import BaseModel
from typing import Optional


class ForgotPasswordRequest(BaseModel):
    username: str  # Kita gunakan username seperti dalam login


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
    confirm_new_password: str


class ChangePasswordRequest(BaseModel):
    username: str
    new_password: str
    confirm_new_password: str


class PasswordResetResponse(BaseModel):
    message: str
    token: Optional[str] = None