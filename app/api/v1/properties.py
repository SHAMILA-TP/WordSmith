import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.errors import NotFoundError
from app.models import Property
from app.schemas.property import PropertyOut

router = APIRouter(prefix="/properties", tags=["properties"])


@router.get("/{property_id}", response_model=PropertyOut)
def get_property(property_id: uuid.UUID, db: Session = Depends(get_db)):
    prop = db.get(Property, property_id)
    if prop is None:
        raise NotFoundError("Property not found")
    return prop
