from pydantic import BaseModel

class ConsentRequest(BaseModel):
    user_id: str
    password: str
