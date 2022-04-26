from fastapi import HTTPException
import time
import app.myjwt as myjwt
from typing import Any

test_user = {
    "user_id": "test_user_id",
    "password": "test_pass",
    "email": "i_need_this@mail.com",
}
user_dict = {test_user["user_id"]: test_user}

test_authorization_code = "THIS_IS_AUTHORIZATION_CODE"


def is_correct_user(user_id: str, password: str) -> bool:
    return user_id == test_user["user_id"] and password == test_user["password"]


def consent(user_id: str, password: str) -> str:
    if is_correct_user(user_id, password):
        return test_authorization_code
    else:
        raise HTTPException(status_code=401, detail="user id or password is wrong.")


def create_payload() -> dict[str, Any]:
    iat = int(time.time())
    duration = 600
    exp = int(iat + duration)
    return {
        "exp": exp,
        "iat": iat,
        "iss": "auth-server-service",
        "sub": test_user["user_id"],
    }


def token(authorization_code: str) -> str:
    if authorization_code == test_authorization_code:
        payload = create_payload()
        print(payload)
        return myjwt.encode(payload)
    else:
        raise HTTPException(status_code=401, detail="Invalid authorization code.")


def get_email(id_token: str) -> str:
    try:
        payload = myjwt.decode(id_token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid id token")
    user_id = payload["sub"]
    email = user_dict[user_id]["email"]
    return email
