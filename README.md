# 📜 Proposal Service

`ProposalService` is a microservice responsible for creating, updating, and retrieving freelancer proposals for projects on a platform. It is part of a microservice architecture, communicates with other services via gRPC, publishes events to Kafka, and interacts with PostgreSQL using async SQLAlchemy.

---

## 📆 Tech Stack

* **Python 3.11**
* **FastAPI** — Async REST API
* **SQLAlchemy 2.0 (async) + Alembic**
* **PostgreSQL**
* **gRPC (aio)** — Client to ProjectService
* **Kafka (confluent-kafka)**
* **Docker + Docker Compose**
* **Domain-Driven Design (DDD)** + Layered Architecture

---

## 📁 Project Structure

```
app/
├── domain/                  # Entities and interfaces
├── infrastructure/         # DB, Kafka, gRPC, logging, security implementations
├── services/               # Business logic layer
├── presentation/           # HTTP API layer (FastAPI)
├── proto/                  # gRPC protocol definitions
├── generated/              # Generated protobuf files
├── config/                 # Kafka & environment settings
├── cmd/                    # Application entrypoint
├── test/                   # Unit test scaffolding
alembic/                    # Database migrations
```

---

## 🚀 Functionality

### 🔧 REST API (FastAPI)

| Method  | Endpoint                  | Description                   |
| ------- | ------------------------- | ----------------------------- |
| `POST`  | `/proposals/`             | Create a proposal             |
| `PATCH` | `/proposals/{id}`         | Update proposal status        |
| `GET`   | `/proposals/{id}`         | Retrieve a single proposal    |
| `GET`   | `/proposals/project/{id}` | Get all proposals for project |

### 📱 gRPC Client

* When creating a proposal, a gRPC call is made to **ProjectService** to validate the project ID.

### 📨 Kafka Events

* After successful proposal creation, a `proposal.created` event is published:

```json
{
  "proposal_id": "uuid",
  "project_id": "uuid",
  "freelancer_id": "uuid",
  "status": "pending",
  "timestamp": "..."
}
```

---

## 📆 Getting Started

### 🔗 Prerequisites

* Docker
* Docker Compose

### 📄 .env File (app/.env)

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@proposal_db:5432/proposals_db
POSTGRES_DB=proposals_db
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
PROJECT_GRPC_HOST=grpc_server
PROJECT_GRPC_PORT=50051
```

### 🚀 Start the Service (from root directory)

```bash
# Build the services
make build

# Start the services
make up

# View logs
make logs

# Run migrations
make migrate
```

---

## ✅ Example Request

```http
POST /proposals/
Content-Type: application/json

{
  "project_id": "uuid",
  "message": "I'm ready to take on this project",
  "price": 1500.0,
  "estimated_days": 10
}
```

---

## 📊 Architecture Notes

* **DDD**: Clear separation of domain / service / infrastructure / presentation
* **Kafka**: Pluggable producer with lifecycle integration
* **gRPC**: Lazy client initialization (`await self.init()`)
* **PostgreSQL**: asyncpg + SQLAlchemy 2.0 + Alembic for migrations

---
