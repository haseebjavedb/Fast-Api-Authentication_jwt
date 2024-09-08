from pydantic import BaseModel

class ItemResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True

class ItemCreate(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username:str
    email:str
    password:str
    token:str

class UserLogin(BaseModel):
    username:str
    email:str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str
    message:str

class TokenData(BaseModel):
    username: str | None = None       
