from pydantic import BaseModel

class User(BaseModel):
    mobile: str
    otp: str