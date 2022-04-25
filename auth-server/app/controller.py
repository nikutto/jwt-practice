from fastapi import APIRouter, Response, status
from app.request_entity import ConsentRequest, TokenRequest
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
    return {"jwt": ret}

@router.post("/oauth/verify")
async def verify():
    return Response(status_code=status.HTTP_200_OK) # TODO: verify jwt token
