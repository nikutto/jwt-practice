from fastapi import APIRouter, Response, status

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello world"}

@router.post("/oauth/authorize")
async def authorize():
    return {"jwt": "XXX.YYY.ZZZ"} # TODO: return real jwt token

@router.post("/oauth/verify")
async def verify():
    return Response(status_code=status.HTTP_200_OK) # TODO: verify jwt token
