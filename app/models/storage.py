from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Dict

# ==============================
# Pydantic Models
# ==============================


class Customer(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime


class Ticket(BaseModel):
    id: int
    customer_id: int
    subject: str
    description: str
    status: str = "open"
    created_at: datetime
    updated_at: datetime


class TicketNote(BaseModel):
    id: int
    ticket_id: int
    text: str
    created_at: datetime


# ==============================
# In-Memory Storage
# ==============================


class MemoryStore:
    def __init__(self):
        self.customers: Dict[int, Customer] = {}
        self.tickets: Dict[int, Ticket] = {}
        self.notes: Dict[int, TicketNote] = {}

        self.customer_id = 1
        self.ticket_id = 1
        self.note_id = 1

    # Customer ops
    def create_customer(self, name: str, email: str) -> Customer:
        customer = Customer(
            id=self.customer_id, name=name, email=email, created_at=datetime.utcnow()
        )
        self.customers[self.customer_id] = customer
        self.customer_id += 1
        return customer

    def get_customer(self, cid: int) -> Customer:
        return self.customers[cid]

    # Ticket ops
    def create_ticket(self, customer_id: int, subject: str, description: str) -> Ticket:
        ticket = Ticket(
            id=self.ticket_id,
            customer_id=customer_id,
            subject=subject,
            description=description,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.tickets[self.ticket_id] = ticket
        self.ticket_id += 1
        return ticket

    def update_ticket(self, tid: int, **updates) -> Ticket:
        ticket = self.tickets[tid]
        for k, v in updates.items():
            setattr(ticket, k, v)
        ticket.updated_at = datetime.utcnow()
        return ticket

    def list_tickets(self, customer_id: Optional[int] = None):
        if customer_id:
            return [t for t in self.tickets.values() if t.customer_id == customer_id]
        return list(self.tickets.values())

    # Notes ops
    def add_note(self, ticket_id: int, text: str) -> TicketNote:
        note = TicketNote(
            id=self.note_id, ticket_id=ticket_id, text=text, created_at=datetime.utcnow()
        )
        self.notes[self.note_id] = note
        self.note_id += 1
        return note


# Global Singleton
STORE = MemoryStore()
