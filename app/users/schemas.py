from pydantic import BaseModel, EmailStr


class SchemeUserInfo(BaseModel):
    id: int
    email: EmailStr


class SchemeUserAuth(BaseModel):
    email: EmailStr
    password: str
