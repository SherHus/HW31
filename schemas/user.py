from pydantic import BaseModel


class UserSchema(BaseModel):
    full_name: str
    username: str
    password: str


class UserSignInSchema(BaseModel):
    username: str
    password: str
