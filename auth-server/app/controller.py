from typing import Optional
from fastapi import APIRouter, Header, HTTPException
from app.request_entity import ConsentRequest, TokenRequest
import re
import app.service as service

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello world"}

@router.post("/oauth/consent")
async def consent(consent_request: ConsentRequest):
    ret = service.consent(consent_request.user_id, consent_request.password)
    return {"authorization_code": ret}

@router.post("/oauth/token")
async def token(token_request: TokenRequest):
    ret = service.token(token_request.authorization_code)
    return {"id_token": ret}

@router.get("/api/profile/email")
async def profile(authorization: Optional[str] = Header(None)):
    if authorization is None:
        raise HTTPException(status_code = 401, details = "Need Authorization header.")
    match = re.fullmatch(r" Bearer (.*)", authorization)
    if match is None:
        raise HTTPException(status_code = 401, detail = "Not valid format. The valid format is 'Authorization: Bearer <id_token>'")
    id_token = match.group(1)

    email = service.get_email(id_token)

    return {"email": email}
