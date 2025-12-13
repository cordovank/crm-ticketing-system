# Smoke Test Pack – CRM/Ticketing System

This smoke test pack validates that the **CRM/Ticketing System** backend is correctly wired with:

* Authentication middleware
* Role-Based Access Control (RBAC)
* In-memory data store
* Core CRM/Ticketing API flows

These tests are designed to quickly verify **backend correctness and security behavior** before integrating UI or downstream services.

---

## ✅ Smoke Test Plan

The following functionality is verified:

* Health check
* Authentication behavior
* RBAC enforcement
* Customer retrieval
* Ticket creation
* Ticket listing
* Ticket update
* Note creation
* Unauthorized access handling

> All tests assume the server is running with authentication and RBAC enabled.

---

## 🔧 Prerequisites

### 1️⃣ Start the server

```bash
uvicorn app.main:app --reload
```

The server should be available at:

```
http://localhost:8000
```

---

### 2️⃣ Run the smoke test script

```bash
chmod +x scripts/smoke.sh
./scripts/smoke.sh
```

> The script assumes the backend is already running.

---

## 🧪 Smoke Tests (Manual Reference)

The following commands document the expected behavior and can be run manually if needed.

---

### 0️⃣ Invalid Endpoint

Unknown routes should return `404 Not Found`.

```bash
curl -X GET http://localhost:8000/
```

Expected response:

```json
{"detail":"Not Found"}
```

---

### 1️⃣ Health Check (No Auth Required)

```bash
curl -X GET http://localhost:8000/health
```

Expected response:

```json
{"status":"ok"}
```

Validates:

* Server is running
* Health endpoint is public
* No authentication required

---

### 2️⃣ Unauthorized Access (RBAC Enforcement)

Accessing protected endpoints without a token should fail.

```bash
curl -X GET http://localhost:8000/api/customers/1
```

Expected response:

```json
{"detail":"Forbidden: role 'None' unauthorized"}
```

Validates:

* Auth middleware is active
* RBAC enforcement is working

---

### 3️⃣ Authorized Access (Agent Token, No Data)

Attempt to retrieve a customer before validating seed behavior.

```bash
curl -H "Authorization: Bearer agent123" \
     http://localhost:8000/api/customers/1
```

If no seeds are present, expected response:

```json
{"detail":"Customer not found"}
```

> Note: The in-memory store resets on each server restart.

---

### 4️⃣ Customer Retrieval (Seeded Data)

Seeded customers are added at startup in `app/main.py`.

```bash
curl -H "Authorization: Bearer agent123" \
     http://localhost:8000/api/customers/1
```

Expected response:

```json
{
  "id": 1,
  "name": "Jane Doe",
  "email": "jane@example.com",
  "created_at": "2024-06-01T12:00:00Z"
}
```

Validates:

* Seed data initialization
* Customer retrieval endpoint
* Auth + RBAC enforcement

---

### 5️⃣ Ticket Creation (Auth Required)

Agents can create tickets for existing customers.

```bash
curl -X POST http://localhost:8000/api/tickets/ \
  -H "Authorization: Bearer agent123" \
  -H "Content-Type: application/json" \
  -d '{
        "customer_id": 1,
        "subject": "Laptop not booting",
        "description": "Customer reports system will not start."
      }'
```

Expected response:

```json
{
  "id": 1,
  "customer_id": 1,
  "subject": "Laptop not booting",
  "description": "Customer reports system will not start.",
  "status": "open",
  "created_at": "...",
  "updated_at": "..."
}
```

Validates:

* Ticket creation flow
* Customer existence validation
* Auth + RBAC enforcement

---

### 6️⃣ Ticket Listing (Public Endpoint)

Ticket listing is publicly accessible.

```bash
curl -X GET http://localhost:8000/api/tickets/
```

Expected response:

```json
[
  {
    "id": 1,
    "customer_id": 1,
    "subject": "Laptop not booting",
    "description": "Customer reports system will not start.",
    "status": "open",
    "created_at": "...",
    "updated_at": "..."
  }
]
```

Validates:

* Ticket listing endpoint
* Public access behavior

---

### 7️⃣ Ticket Update (Auth Required)

Agents can update ticket status.

```bash
curl -X PATCH http://localhost:8000/api/tickets/1 \
  -H "Authorization: Bearer agent123" \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'
```

Expected response:

```json
{
  "id": 1,
  "customer_id": 1,
  "subject": "Laptop not booting",
  "description": "Customer reports system will not start.",
  "status": "in_progress",
  "created_at": "...",
  "updated_at": "..."
}
```

Validates:

* Ticket update endpoint
* Auth + RBAC enforcement

---

### 8️⃣ A. Note Creation (Auth Required)

Admins (or agents) can add notes to tickets.

```bash
curl -X POST http://localhost:8000/api/notes/1 \
  -H "Authorization: Bearer admin123" \
  -H "Content-Type: application/json" \
  -d '{"text": "Customer called back with additional details."}'
```

Expected response:

```json
{
  "data": {
    "id": 1,
    "ticket_id": 1,
    "text": "Customer called back with additional details.",
    "created_at": "..."
  }
}
```

Validates:

* Note creation endpoint
* Auth + RBAC enforcement

---

### 8️⃣ B. Note Creation (Unauthorized Fails)

```bash
curl -X POST http://localhost:8000/api/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"text": "Unauthorized attempt"}'
```

Expected response:

```json
{"detail":"Forbidden: role 'None' unauthorized"}
```

Validates:

* Unauthorized access is blocked
* RBAC enforcement is consistent

---

## 🧠 Notes

* All data is **in-memory** and resets on restart
* IDs increment per run
* Smoke tests are intended to validate **behavior, not persistence**
* This pack should be run **before UI or integration testing**

---

### ✅ Status

If all tests pass, the **CRM/Ticketing System backend is fully operational** and ready for downstream use.
