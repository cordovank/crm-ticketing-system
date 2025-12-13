# **CRM/Ticketing System**

**Lightweight enterprise CRM and ticketing microservice with a FastAPI backend and Gradio-based UI.**

This project provides a **self-contained CRM/Ticketing system** designed to model common enterprise backend patterns, including authenticated APIs, role-based access control, structured domain operations, and a simple user interface for interaction.

---

## 📌 **Overview**
The CRM/Ticketing system simulates a backend service for managing customers, support tickets, and associated notes. It features token-based authentication with role-based access control (RBAC) to restrict operations based on user roles (e.g., "agent", "admin").

Key features include:
* **FastAPI backend** exposing customer, ticket, and note APIs
* **Token-based authentication with RBAC**
* **In-memory data storage** with seeded demo data
* **Gradio UI** for interacting with the system
* **Deterministic, role-aware operations**

This service can be used as:

* A backend service for enterprise integrations
* A mock CRM for testing automation pipelines
* A reference architecture for RBAC-enabled microservices
* A foundation for future extensions (agents, workflows, integrations)

---

## 🧱 **Architecture**

```
├── app/
│   ├── config.py               → Settings, tokens, environment
│   ├── main.py                 → FastAPI application entrypoint + startup logic
│   ├── api/
│   │   ├── customers.py        → Customer retrieval
│   │   ├── tickets.py          → Ticket CRUD operations
│   │   ├── notes.py            → Ticket notes management
│   │   └── router.py           → Master API router
│   ├── auth/
│   │   ├── middleware.py       → Bearer token auth + role injection
│   │   └── rbac.py             → Role-Based Access Control helper
│   ├── models/
│   │   └── storage.py          → In-memory store
│   └── utils/
│       └── exceptions.py       → Consistent API error responses
│
├── scripts/
│   └── smoke.sh                → Automated backend verification script
│
├── ui/
│   └── gradio_app.py           → User-facing UI for interacting with AI agent
│
├── .env
├── README.md
├── pyproject.toml
└── uv.lock
```

---

## 🛠 **Setup**

### 1️⃣ Clone the repository

```bash
git clone https://github.com/cordovank/crm-ticketing-system.git
cd crm-ticketing-system
```

### 2️⃣ Install dependencies (UV)

```bash
uv sync
source .venv/bin/activate
```

### 3️⃣ Environment configuration (optional)

Create a `.env` file if you want to override defaults (tokens, ports, etc.).

---

## ▶️ **Running the Services**

### **FastAPI Backend**

```bash
uv run uvicorn app.main:app --reload --port 8000
```

Health check:

```bash
curl http://localhost:8000/health
```

---

### **Gradio UI**

```bash
uv run python ui/gradio_app.py
# or
uv run crmsys-ui
```

Access the UI at:

```
http://127.0.0.1:7861
```

---

## 🔐 **Authentication & RBAC**

The backend uses **Bearer token authentication** with role enforcement.

### Tokens

```
Authorization: Bearer agent123
Authorization: Bearer admin123
```

### Roles

| Token    | Role  |
| -------- | ----- |
| agent123 | agent |
| admin123 | admin |

---

### Permissions

| Operation       | Required Role |
| --------------- | ------------- |
| Get customer    | agent, admin  |
| Create ticket   | agent, admin  |
| Update ticket   | agent, admin  |
| Add ticket note | agent, admin  |
| List tickets    | public        |

All authorization is enforced at the API layer.

---

## 🗃 **Data Model**

* All data is stored **in-memory**
* Automatically **seeded at startup**
* Reset on server restart

Seeded entities include:

* Customers (e.g., IDs `1`, `2`)
* Tickets and notes created during runtime

This design keeps the service **stateless and deterministic**, ideal for demos and testing.

---

## 🧪 **Smoke Test**

An automated smoke test validates the backend end-to-end.

```bash
chmod +x scripts/smoke.sh
./scripts/smoke.sh
```

The script verifies:

* Health endpoint availability
* Authentication enforcement
* RBAC behavior
* Seeded customer retrieval
* Ticket creation and updates
* Ticket listing
* Note creation
* Unauthorized access handling

All tests assume the backend is already running.

---

## 🧠 **Example Usage Flow**

1. Retrieve a customer:

   ```bash
   GET /customers/1
   ```

2. Create a ticket:

   ```bash
   POST /tickets
   ```

3. Update ticket status:

   ```bash
   PATCH /tickets/{ticket_id}
   ```

4. Add a note to a ticket:

   ```bash
   POST /notes/{ticket_id}
   ```

View results via the Gradio UI or direct API calls.


> ⚠️ This service is intended for demonstration, testing, and reference purposes.
> It is not production-hardened and omits persistence, auditing, and advanced security controls.
