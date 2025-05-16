from fastapi import APIRouter
from app.api.v1.endpoints import health, generate_sql, schema

api_router = APIRouter()

# Include API endpoints
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(generate_sql.router, prefix="/generate-sql", tags=["sql"])
api_router.include_router(schema.router, prefix="/schema", tags=["schema"])
