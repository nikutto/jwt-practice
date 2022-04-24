from typing import Optional
from fastapi import APIRouter, Response, Header, status
from app.request_entity import ConsentRequest
import app.service as service

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello world"}

@router.post("/oauth/consent")
async def consent(consent_request: ConsentRequest):
    ret = service.consent(consent_request.user_id, consent_request.password)
    return {"authorization_code": ret}

@router.post("/oauth/authorize")
async def authorize():
    return {"jwt": "XXX.YYY.ZZZ"} # TODO: return real jwt token

@router.post("/oauth/verify")
async def verify():
    return Response(status_code=status.HTTP_200_OK) # TODO: verify jwt token
