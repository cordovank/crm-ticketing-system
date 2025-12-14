---
title: CRM & Ticketing System
emoji: 🧩
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
short_description: Contenerized FastAPI CRM & Ticketing API with Gradio UI

---

## CRM & Ticketing System — Interactive Demo

This Space hosts an interactive Gradio UI backed by a FastAPI CRM & Ticketing service.

For demo purposes, both the backend service and the UI are deployed within a **single Docker container**, allowing the UI to communicate with the API over an internal network.

---

## What’s Running Here

- FastAPI CRM backend (Docker image)
- Gradio UI client
- Internal API calls via `http://localhost:8000`

---

## Architecture (Demo Mode)

```text
+---------------------------+
|   Hugging Face Docker     |
|                           |
|  +---------------------+ |
|  |  Gradio UI (7860)   | |
|  +----------+----------+ |
|             |            |
|             v            |
|  +---------------------+ |
|  | FastAPI CRM (8000)  | |
|  +---------------------+ |
+---------------------------+
```

* **FastAPI CRM:**
  Backend service exposing customer, ticket, and note management endpoints.

* **UI:**
  A Gradio application that interacts with the backend via HTTP calls.

* **Deployment Model:**
  The container extends a published backend Docker image and layers the UI on top, running both services together for seamless interaction.

---

## Notes
* This combined deployment is for interactive demo purposes
* The backend is designed to run independently in production
* The same backend image is reused by agents and other clients

---

## Roles

| Token    | Role  |
| -------- | ----- |
| agent123 | agent |
| admin123 | admin |

Tokens are preconfigured for demo convenience.

---

## Getting Started

Once the Space is running:

* Use the UI tabs to explore customer data, manage tickets, and add notes
* Role-based access is simulated via predefined tokens to reflect enterprise-style access patterns

