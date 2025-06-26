from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from firebase_admin import auth as firebase_auth
import requests
from app.core.config import FIREBASE_WEB_API_KEY, send_email

router = APIRouter(prefix="/auth", tags=["auth"])

class SignupRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ChangePasswordRequest(BaseModel):
    id_token: str
    new_password: str

@router.post("/signup")
def signup(data: SignupRequest):
    try:
        user = firebase_auth.create_user(email=data.email, password=data.password)
        return {"message": "User created.", "uid": user.uid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(data: LoginRequest):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
    payload = {
        "email": data.email,
        "password": data.password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json().get("error", {}).get("message", "Login failed"))

@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest):
    try:
        link = firebase_auth.generate_password_reset_link(data.email)
        subject = "Password Reset Request"
        body = f"Click the following link to reset your password: {link}"
        send_email(data.email, subject, body)
        return {"message": "Password reset email sent."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/change-password")
def change_password(data: ChangePasswordRequest):
    try:
        decoded_token = firebase_auth.verify_id_token(data.id_token)
        uid = decoded_token["uid"]
        firebase_auth.update_user(uid, password=data.new_password)
        return {"message": "Password updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/verify-email")
def verify_email(email: EmailStr):
    try:
        link = firebase_auth.generate_email_verification_link(email)
        # TODO: Send 'link' to user's email using Firebase built-in method
        return {"message": "Verification email sent."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 