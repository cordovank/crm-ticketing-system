# **CRM & Ticketing System**

**A standalone, Dockerized CRM & Ticketing backend built with FastAPI, designed to be reusable across UIs, agents, and external integrations.**

The project demonstrates clean service boundaries, containerized deployment, and UI/API decoupling following real-world enterprise patterns, including authenticated APIs, role-based access control, structured domain operations, and a simple user interface for interaction.

Demo: https://huggingface.co/spaces/cordovank/crmsys

---

## 📌 **Overview**
This repository contains the **CRM backend service** only.

* **FastAPI-based REST API** exposing customer, ticket, and note APIs
* **Token-based authentication with RBAC** (agent / admin)
* **In-memory data storage** with seeded demo data
* **Dockerized** for reproducible deployment
* Designed for integration with UIs and LLM agents

A **Gradio-based UI** is deployed separately on Hugging Face Spaces as a client of this API.

---

## 🧱 **Architecture**

```text
+-------------------+        HTTP        +----------------------+
|   UI / Agent      |  ─────────────▶   |   CRM API Service    |
|  (Gradio, LLM)    |                   |  (FastAPI, Docker)  |
+-------------------+                   +----------------------+
```

The backend is intentionally UI-agnostic and can be consumed by:
* Web UIs
* Agent services
* Integration tests
* Other microservices

---

## API Features

* **Customers**: Retrieve customer records
* **Tickets**: Create, list, update tickets
* **Notes**: Add notes to tickets
* **Health**: `/health` endpoint for readiness checks

---

## Run Locally with Docker

```bash
# build the image
docker build -t cordn29/crmsys:0.2.0 .

# run the service
docker run -p 8000:8000 cordn29/crmsys:0.2.0
```

**Verify**
* **API docs:** http://localhost:8000/docs
* **Health:** http://localhost:8000/health

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
python ui/gradio_app.py
```

Access the UI at:

```
http://127.0.0.1:7861
```

---

## 🔐 **Authentication & RBAC (Simulated)**

The API uses **Bearer token authentication** with role enforcement.

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

### Example

```bash
curl -H "Authorization: Bearer agent123" http://localhost:8000/api/customers/1
```

---

## Docker Image

The backend is published as a reusable Docker image :

```bash
docker pull cordn29/crmsys:0.2.0
docker pull cordn29/crmsys:0.2.0-amd64
```

---

## Related Deployments

**UI Demo (Hugging Face Spaces):** A combined Docker Space layers a Gradio UI on top of this backend image for interactive demos.


> ⚠️ This service is intended for demonstration, testing, and reference purposes.
> It is not production-hardened and omits persistence, auditing, and advanced security controls.
