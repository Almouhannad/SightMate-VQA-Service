from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field

class ApiKey(BaseModel):
    """
    API Key domain model
    """
    id: Optional[str] = None
    hashed_key: str
    key_prefix: str # For effecient search
    initialized_in: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_use_in: Optional[datetime] = None
    number_of_requests: int = 0

    def update_usage(self,
                     last_use_in: Optional[datetime] = None,
                     increment: int = 1):
        if (last_use_in is None):
            last_use_in = datetime.now(timezone.utc)
        self.last_use_in = last_use_in
        self.number_of_requests += increment
        return self