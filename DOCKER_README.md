## Dockerized Service

The CRM & Ticketing API is packaged as a standalone Docker image and can be run independently as a reusable backend service.

The image is published on Docker Hub and exposes a FastAPI-based REST API.

---

## Run with Docker

### Build locally
```bash
docker build -t cordn29/crmsys:0.1.0 .
docker tag cordn29/crmsys:0.1.0 cordn29/crmsys:latest
```

### Run the service
```bash
docker run -p 8000:8000 cordn29/crmsys:latest
```

Once running, the API is available at:
* OpenAPI docs: http://localhost:8000/docs
* Health check: http://localhost:8000/health

---

## Docker Image

The CRM service is published as a reusable Docker image:

```bash
docker pull cordn29/crmsys:latest
```

This image can be consumed by other services

---

## Validation

### Health check
```bash
curl http://localhost:8000/health
```

```json
{"status":"ok"}
```

### Authorized API access
```bash
curl -H "Authorization: Bearer agent123" http://localhost:8000/api/customers/1
```

```json
{
  "id": 1,
  "name": "Jane Doe",
  "email": "jane@example.com",
  "created_at": "2025-12-13T08:29:47.914133"
}
```

---

## Authentication

The API uses a simple bearer-token mechanism to simulate role-based access control.

Example tokens:
- `agent123` — agent role
- `admin123` — admin role

This is intended to model enterprise-style API access and will be extended in future integrations.