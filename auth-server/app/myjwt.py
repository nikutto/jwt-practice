import base64
import json
import hashlib
import hmac
import time
from typing import Any


def base64url_encode(s: str) -> str:
    s_bytes = s.replace(" ", "").encode()
    return base64.urlsafe_b64encode(s_bytes).decode().replace("=", "")


def create_header() -> dict[str, Any]:
    return {"alg": "HW256", "typ": "JWT"}


key = "secret"


def create_sign(msg: str) -> str:
    sign = hmac.new(key.encode(), msg.encode(), hashlib.sha256).digest()
    return base64.urlsafe_b64encode(sign).decode().replace("=", "")


def encode_dict(d: dict[str, Any]) -> str:
    dumped_str = json.dumps(d, sort_keys=True, separators=(",", ":"))
    return base64url_encode(dumped_str)


def decode_dict(s: str) -> dict[str, Any]:
    s = s + "".join(["=" for _ in range(len(s) % 4)])
    decoded_str = base64.urlsafe_b64decode(s.encode()).decode()
    print(decoded_str)
    return json.loads(decoded_str)  # type: ignore


def encode(payload: dict[str, Any]) -> str:
    header = encode_dict(create_header())
    payload_str = encode_dict(payload)
    sign = base64url_encode(create_sign(f"{header}.{payload_str}"))
    my_token = f"{header}.{payload_str}.{sign}"

    return my_token


def decode(id_token: str) -> dict[str, Any]:
    lst = id_token.split(".")
    if len(lst) != 3:
        raise ValueError("jwt format is wrong.")
    [header, payload, sign] = lst

    if base64url_encode(create_sign(f"{header}.{payload}")) != sign:
        raise ValueError("Sign is wrong.")

    header_dict = decode_dict(header)
    payload_dict = decode_dict(payload)
    if header_dict != create_header():
        raise ValueError("Header is wrong.")

    now = time.time()
    if payload_dict["exp"] < now:
        raise ValueError("Expired.")

    return payload_dict
