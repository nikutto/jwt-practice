from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.post("/oauth/authorize")
async def authorize():
    return {"jwt": "XXX.YYY.ZZZ"} # TODO: return real jwt token
