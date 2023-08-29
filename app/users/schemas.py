from pydantic import BaseModel, EmailStr


class SchemeUserRegister(BaseModel):
    email: EmailStr
    password: str
