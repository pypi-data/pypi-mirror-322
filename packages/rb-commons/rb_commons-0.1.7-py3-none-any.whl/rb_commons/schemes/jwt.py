import uuid
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class UserRole(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    GUEST = "guest"

class Claims(BaseModel):
    model_config = ConfigDict(extra="ignore")

    user_id: str = Field(None, alias="x-user-id")
    user_role: UserRole = Field(UserRole.GUEST, alias="x-user-role")
    shop_id: uuid.UUID = Field(None, alias="x-shop-id")
