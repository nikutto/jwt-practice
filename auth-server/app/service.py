from fastapi import HTTPException
from app.request_entity import ConsentRequest

test_user = {
    "user_id": "test_user_id",
    "password": "test_pass"
}
authorization_code = "THIS_IS_AUTHORIZATION_CODE"

def is_correct_user(user_id: str, password: str): # TODO
    return user_id == test_user["user_id"] and password == test_user["password"]

def consent(user_id: str, password: str):
    if is_correct_user(user_id, password):
        return authorization_code # TODO: return real authentication_token
    else:
        raise HTTPException(status_code = 401, detail = "user id or password is wrong.")
