import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PropertyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    brand_id: uuid.UUID
    name: str
    property_term: str
    communication_guidelines: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
