import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.errors import NotFoundError
from app.models import Brand, Property
from app.schemas.brand import BrandOut
from app.schemas.property import PropertyOut

router = APIRouter(prefix="/brands", tags=["brands"])


@router.get("", response_model=list[BrandOut])
def list_brands(include_inactive: bool = False, db: Session = Depends(get_db)):
    query = select(Brand).order_by(Brand.name)
    if not include_inactive:
        query = query.where(Brand.is_active.is_(True))
    return db.scalars(query).all()


@router.get("/{brand_id}", response_model=BrandOut)
def get_brand(brand_id: uuid.UUID, db: Session = Depends(get_db)):
    brand = db.get(Brand, brand_id)
    if brand is None:
        raise NotFoundError("Brand not found")
    return brand


@router.get("/{brand_id}/properties", response_model=list[PropertyOut])
def list_brand_properties(brand_id: uuid.UUID, db: Session = Depends(get_db)):
    if db.get(Brand, brand_id) is None:
        raise NotFoundError("Brand not found")
    query = (
        select(Property).where(Property.brand_id == brand_id).order_by(Property.name)
    )
    return db.scalars(query).all()
