from fastapi import APIRouter, Request, HTTPException
from app.models.storage import STORE, Customer
from app.auth.rbac import require_role

router = APIRouter()


@router.get("/{customer_id}", response_model=Customer)
def get_customer(request: Request, customer_id: int):
    # RBAC: Only authenticated agents/admins can view customers
    require_role(request, ["agent", "admin"])

    try:
        return STORE.get_customer(customer_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Customer not found")
