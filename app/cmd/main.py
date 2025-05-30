# app/cmd/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

from app.presentation.http.proporsal_handler import router as project_router
from app.presentation.http.exception_handlers import (
    project_not_open,
    proposal_already_accepted,
    proposal_already_exists,
    proposal_not_found,
    unauthorized_proposal_access,

)
from app.infrastructure.security.middleware import JWTAuthMiddleware
from app.domain.exceptions import ProjectNotOpen, ProposalAlreadyAccepted, ProposalAlreadyExists, ProposalNotFound, UnauthorizedProposalAccess

from app.infrastructure.logger.logger import get_logger
from app.infrastructure.kafka.kafka_topic_manager import KafkaTopicManager
from app.infrastructure.kafka.kafka_producer import KafkaProducer
from app.config.kafka_config import KAFKA_TOPICS
import asyncpg
from sqlalchemy.exc import OperationalError, DBAPIError
from app.infrastructure.db.db_session import engine
from sqlalchemy import text

logger = get_logger("UserService")
async def wait_for_db(max_retries=10, delay=2):
    for attempt in range(max_retries):
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
                logger.info("✅ Database is ready!")
                return
        except (OperationalError, DBAPIError, asyncpg.PostgresError) as e:
            logger.warning(f"❌ DB not ready (attempt {attempt + 1}/{max_retries}) — {e}")
            await asyncio.sleep(delay)
    raise RuntimeError("❌ Could not connect to the database after retries")
@asynccontextmanager
async def lifespan(app: FastAPI):
    await wait_for_db()
    logger = get_logger("lifespan")
    logger.info("FastAPI lifespan started")

    # Kafka topic init
    topic_manager = KafkaTopicManager(logger=logger)
    await topic_manager.create_topics(list(KAFKA_TOPICS.values()))

    # Kafka producer
    kafka_producer = KafkaProducer(bootstrap_servers="kafka:9092", logger=logger)
    await kafka_producer.connect()
    app.state.kafka_producer = kafka_producer

    yield

    logger.info("FastAPI lifespan stopped")
    await kafka_producer.stop()


app = FastAPI(lifespan=lifespan)
app.add_middleware(JWTAuthMiddleware)
app.include_router(project_router)

app.add_exception_handler(ProjectNotOpen, project_not_open)
app.add_exception_handler(ProjectNotOpen, proposal_already_accepted)
app.add_exception_handler(ProposalAlreadyExists, proposal_already_exists)
app.add_exception_handler(ProposalNotFound, proposal_not_found)
app.add_exception_handler(UnauthorizedProposalAccess, unauthorized_proposal_access)

