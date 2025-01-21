import uuid
from enum import Enum
from pydantic import BaseModel, Field


class UserRole(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    GUEST = "guest"

class Claims(BaseModel):
    user_id: str = Field(None, alias="x-user-id")
    user_role: UserRole = Field(UserRole.GUEST, alias="x-user-role")
    shop_id: uuid.UUID = Field(None, alias="x-shop-id")

    class Config:
        extra = "ignore"
