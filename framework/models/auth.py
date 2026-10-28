from pydantic import BaseModel, ConfigDict,EmailStr, Field

# class Register(BaseModel):
#     model_config = ConfigDict(extra='forbid', strict=True)
#     email: str
#     password: str

class User(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)

    id: str
    email: EmailStr
    created_at: str