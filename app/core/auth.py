from fastapi import Depends, HTTPException, status, Request
from firebase_admin import auth as firebase_auth

def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    id_token = auth_header.split(" ")[1]
    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        return {"uid": decoded_token["uid"], "email": decoded_token.get("email")}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token") 