from fastapi import (
    FastAPI,
    Response,
    status
)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.post("/oauth/authorize")
async def authorize():
    return {"jwt": "XXX.YYY.ZZZ"} # TODO: return real jwt token

@app.post("/oauth/verify")
async def verify():
    return Response(status_code=status.HTTP_200_OK) # TODO: verify jwt token
