# app/services/dependencies.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.db_session import get_session
from app.infrastructure.db.postgres_project_repository import PostgresqlProposalRepository
from app.infrastructure.logger.logger import get_logger
from app.domain.common.logger import AbstractLogger
from app.infrastructure.kafka.kafka_producer import get_kafka_producer, KafkaProducer
from app.infrastructure.grpc.project_client import ProjectServiceClient
from app.services.proporsal_service import ProposalService


async def get_project_client() -> ProjectServiceClient:
    client = ProjectServiceClient()
    await client.init()
    return client


async def get_proposal_service(
    session: AsyncSession = Depends(get_session),
    logger: AbstractLogger = Depends(get_logger),
    kafka_producer: KafkaProducer = Depends(get_kafka_producer),
    project_client: ProjectServiceClient = Depends(get_project_client),
) -> ProposalService:
    repo = PostgresqlProposalRepository(session=session, logger=logger)
    return ProposalService(
        proposal_repo=repo,
        logger=logger,
        kafka_producer=kafka_producer,
        project_client=project_client,
    )
