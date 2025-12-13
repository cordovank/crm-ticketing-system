from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from app.models.storage import STORE
from app.auth.rbac import require_role

router = APIRouter()


class NoteCreate(BaseModel):
    text: str


@router.post("/{ticket_id}", response_model=dict)
def add_note(req: Request, ticket_id: int, payload: NoteCreate):
    # RBAC: Adding notes requires agent/admin role
    require_role(req, ["agent", "admin"])

    # Ensure ticket exists
    if ticket_id not in STORE.tickets:
        raise HTTPException(404, "Ticket not found")

    note = STORE.add_note(ticket_id, payload.text)
    return {"data": note}
