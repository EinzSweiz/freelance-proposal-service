# 📜 Proposal Service

`ProposalService` — это микросервис для создания, обновления и получения предложений (от фрилансеров) для проектов на платформе. Он является частью микросервисной архитектуры, общается с другими сервисами по gRPC, публикует события в Kafka и работает с PostgreSQL в асинхронном режиме.

---

## 📆 Стек технологий

* **Python 3.11**
* **FastAPI** — REST API (async)
* **SQLAlchemy 2.0 (async) + Alembic**
* **PostgreSQL**
* **gRPC (aio)** — клиент к ProjectService
* **Kafka (confluent-kafka)**
* **Docker + Docker Compose**
* **Domain-Driven Design (DDD)** + слоистая архитектура

---

## 📁 Структура проекта

```
app/
├── domain/                  # Сущности, абстракции
├── infrastructure/         # Реализации: DB, Kafka, gRPC, logging, security
├── services/               # Бизнес-логика
├── presentation/           # HTTP API (FastAPI)
├── proto/                  # gRPC протоколы
├── generated/              # Сгенерированные protobuf
├── config/                 # Kafka/Переменные окружения
├── cmd/                    # Точка входа
├── test/                   # Заготовки для unit-тестов
alembic/                    # Миграции базы
```

---

## 🚀 Функциональность

### 🔧 REST API (FastAPI)

| Method  | Endpoint                  | Description                 |
| ------- | ------------------------- | --------------------------- |
| `POST`  | `/proposals/`             | Создание предложения        |
| `PATCH` | `/proposals/{id}`         | Обновить статус             |
| `GET`   | `/proposals/{id}`         | Получить предложение        |
| `GET`   | `/proposals/project/{id}` | Все предложения для проекта |

### 📱 gRPC-клиент

* При создании proposal делается gRPC-вызов в **ProjectService**, чтобы проверить существование проекта.

### 📨 Kafka Events

* Публикация события `proposal.created`:

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

## 📆 Запуск

### 🔗 Зависимости:

* Docker
* Docker Compose

### 📄 .env (app/.env)

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@proposal_db:5432/proposals_db
POSTGRES_DB=proposals_db
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
PROJECT_GRPC_HOST=grpc_server
PROJECT_GRPC_PORT=50051
```

### 🚀 Запуск из root-папки проекта:

```bash
# Сборка
make build

# Старт
make up

# Логи
make logs

# Миграции
make migrate
```

---

## ✅ Пример запроса

```http
POST /proposals/
Content-Type: application/json

{
  "project_id": "uuid",
  "message": "Готов взяться за проект",
  "price": 1500.0,
  "estimated_days": 10
}
```

---

## 📊 Архитектурные особенности

* **DDD**: разделение domain / service / infra / presentation
* **Kafka**: producer с lifecycle подходом
* **gRPC**: lazy клиент (`await self.init()`)
* **PostgreSQL**: asyncpg + SQLAlchemy 2.0 + Alembic

---
