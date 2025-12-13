from fastapi import FastAPI
from app.api.router import api_router
from app.auth.middleware import AuthMiddleware
from app.utils.exceptions import add_exception_handlers
from app.models.storage import STORE

app = FastAPI(
    title="EnterpriseLink-Agent",
    description="Mock enterprise CRM/Ticketing system for LLM agent integration",
    version="0.1.0",
)


app.add_middleware(AuthMiddleware)  # Auth + logging middleware
app.include_router(api_router)  # Register API router
add_exception_handlers(app)  # Register error handlers


@app.on_event("startup")
def seed_data():
    """
    Seed initial data into the in-memory store.
    Creates customers for smoke tests, removing complexity of customer creation via API.
    """
    STORE.create_customer(name="Jane Doe", email="jane@example.com")
    STORE.create_customer(name="John Smith", email="john@example.com")


@app.get("/health")
def health():
    return {"status": "ok"}
