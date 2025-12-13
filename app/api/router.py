from fastapi import APIRouter
from app.api.customers import router as customers_router
from app.api.tickets import router as tickets_router
from app.api.notes import router as notes_router

api_router = APIRouter(prefix="/api")

api_router.include_router(customers_router, prefix="/customers", tags=["Customers"])
api_router.include_router(tickets_router, prefix="/tickets", tags=["Tickets"])
api_router.include_router(notes_router, prefix="/notes", tags=["Notes"])
