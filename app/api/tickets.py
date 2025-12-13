from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from app.models.storage import STORE, Ticket
from app.auth.rbac import require_role


router = APIRouter()


# ----------------------------
# Request Models
# ----------------------------


class TicketCreate(BaseModel):
    customer_id: int
    subject: str
    description: str


class TicketUpdate(BaseModel):
    subject: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


# ----------------------------
# Routes
# ----------------------------


@router.get("/", response_model=List[Ticket])
def list_tickets(customer_id: Optional[int] = None):
    """
    Listing tickets is safe, doesn't modify state.
    No role required.
    """
    return STORE.list_tickets(customer_id)


@router.post("/", response_model=Ticket)
def create_ticket(request: Request, payload: TicketCreate):
    # RBAC: Ticket creation requires agent/admin role
    require_role(request, ["agent", "admin"])

    # Ensure customer exists
    try:
        STORE.get_customer(payload.customer_id)
    except KeyError:
        raise HTTPException(404, "Customer does not exist")

    return STORE.create_ticket(
        customer_id=payload.customer_id, subject=payload.subject, description=payload.description
    )


@router.patch("/{ticket_id}", response_model=Ticket)
def update_ticket(request: Request, ticket_id: int, payload: TicketUpdate):
    # RBAC: Updating tickets requires agent/admin role
    require_role(request, ["agent", "admin"])

    try:
        ticket = STORE.update_ticket(ticket_id, **payload.dict(exclude_unset=True))
        return ticket
    except KeyError:
        raise HTTPException(404, "Ticket not found")
