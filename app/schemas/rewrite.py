import uuid

from pydantic import BaseModel, ConfigDict, Field


class RewriteRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    brand_id: uuid.UUID
    property_id: uuid.UUID
    draft: str = Field(min_length=1)


class RewriteResponse(BaseModel):
    text: str
    model: str
    prompt_version: str
