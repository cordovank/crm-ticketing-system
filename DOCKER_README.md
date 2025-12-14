## Dockerized Service

The CRM & Ticketing API is packaged as a standalone Docker image and can be run independently as a reusable backend service.

The image is published on Docker Hub and exposes a FastAPI-based REST API.

---

## Run with Docker

### Build locally
```bash
docker build -t cordn29/crmsys:0.2.0 .
docker tag cordn29/crmsys:0.2.0 cordn29/crmsys:latest
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

--- 

## Postmortem: ARM vs AMD64 Docker Image Compatibility

**Summary**
During deployment of the CRM backend to a Hugging Face Docker Space, the container failed at runtime with the following error:

```bash
exec /usr/bin/sh: exec format error
```

**Root Cause**

The original backend Docker image was built on an ARM64 machine (Apple Silicon).
Hugging Face Spaces currently run containers on linux/amd64.

Although the image built and pushed successfully, the runtime attempted to execute ARM64 binaries (including /usr/bin/sh) on an AMD64 host, resulting in an immediate failure.

**Resolution**

A new backend image was built explicitly for linux/amd64 using Docker Buildx and published under a separate tag:

```bash
docker buildx build \
  --platform linux/amd64 \
  -t cordn29/crmsys:0.2.0-amd64 \
  --push \
  .
```

The Hugging Face Space was then updated to reference the AMD64-compatible image:

```bash
FROM cordn29/crmsys:0.2.0-amd64
```

## Lessons Learned
- Docker images are architecture-specific unless explicitly built as multi-arch
- Image registries do not enforce runtime compatibility
- Cloud platforms may differ from local development machines
- Explicit architecture tagging improves portability and auditability