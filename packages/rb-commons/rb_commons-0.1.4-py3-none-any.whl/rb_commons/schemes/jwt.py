import uuid
from enum import Enum
from pydantic import BaseModel

class UserRole(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    GUEST = "guest"

class Claims(BaseModel):
    user_id: str = None
    user_role: UserRole = UserRole.GUEST
    shop_id: uuid.UUID = None
