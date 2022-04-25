import base64
import json
import hashlib
import hmac

def base64url_encode(s: str):
    s_bytes = s.replace(' ', '').encode()
    return base64.urlsafe_b64encode(s_bytes).decode().replace('=', '')

def create_header():
    return {
        "alg": "HW256",
        "typ": "JWT"
    }

key = "secret"
def create_sign(msg: str):    
    sign = hmac.new(key.encode(), msg.encode(), hashlib.sha256).digest()
    return base64.urlsafe_b64encode(sign).decode().replace('=', '')

def encode_dict(d):
    dumped_str = json.dumps(d, sort_keys=True, separators=[':',','])
    return base64url_encode(dumped_str)

def encode(payload):
    header = encode_dict(create_header())
    payload = encode_dict(payload)
    sign = base64url_encode(create_sign(f"{header}.{payload}"))
    my_token = f"{header}.{payload}.{sign}"

    return my_token
