from fastapi import APIRouter, FastAPI

from app.api.v1 import brands, health, properties, rewrite
from app.core.errors import register_exception_handlers

app = FastAPI(title="wordsmith")

register_exception_handlers(app)

app.include_router(health.router)

v1 = APIRouter(prefix="/v1")
v1.include_router(brands.router)
v1.include_router(properties.router)
v1.include_router(rewrite.router)
app.include_router(v1)
