from fastapi import HTTPException
import time
import app.myjwt as myjwt

test_user = {
    "user_id": "test_user_id",
    "password": "test_pass"
}
test_authorization_code = "THIS_IS_AUTHORIZATION_CODE"

def is_correct_user(user_id: str, password: str): # TODO
    return user_id == test_user["user_id"] and password == test_user["password"]

def consent(user_id: str, password: str):
    if is_correct_user(user_id, password):
        return test_authorization_code # TODO: return real authentication_token
    else:
        raise HTTPException(status_code = 401, detail = "user id or password is wrong.")

def create_payload():
    # iat = int(time.time())
    iat = 1650803264
    duration = 600
    exp = int(iat + duration)
    return {
        "exp": exp,
        "iat": iat,
        "iss": "auth-server-service",
        "sub": test_user["user_id"],
    }

def token(authorization_code: str):
    if authorization_code == test_authorization_code:
        payload = create_payload()
        print(payload)
        return myjwt.encode(payload)
    else:
        raise HTTPException(status_code = 401, detail = "Invalid authorization code.")
