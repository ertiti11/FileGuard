from pydantic import BaseModel
from datetime import datetime

class FileUpload(BaseModel):
    filename: str
    file_url: str

    class Config:
        orm_mode = True

class FileResponse(BaseModel):
    id: int
    filename: str
    file_url: str
    uploaded_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str

class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True