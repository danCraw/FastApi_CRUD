from fastapi import APIRouter

from app.api.routes import employees

api_router = APIRouter()

employees_router = APIRouter()
employees_router.include_router(employees.router, prefix="/employees")