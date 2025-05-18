from app.domain.repositories.proporsal_repository import AbstractProposalRepository
from app.domain.entities.proporsal_entity import Proposal, ProposalStatus
from app.domain.common.logger import AbstractLogger
from app.domain.exceptions import (
    ProposalAlreadyExists,
    ProposalNotFound,
    ProjectNotOpen
)
from app.infrastructure.kafka.kafka_producer import KafkaProducer
from app.config.kafka_config import KAFKA_TOPICS
from datetime import datetime
from uuid import UUID


class ProposalService:
    def __init__(
        self,
        proposal_repo: AbstractProposalRepository,
        logger: AbstractLogger,
        kafka_producer: KafkaProducer,
        project_client  # gRPC client to ProjectService
    ):
        self.proposal_repo = proposal_repo
        self.logger = logger
        self.kafka_producer = kafka_producer
        self.project_client = project_client

    async def create_proposal(
        self,
        project_id: UUID,
        freelancer_id: UUID,
        message: str,
        price: float,
        estimated_days: int
    ) -> Proposal:
        # gRPC: check project status
        project = await self.project_client.get_project_by_id(project_id)
        if project["status"] != "open":
            self.logger.warning(f"Project is not open: {project_id}")
            raise ProjectNotOpen("You cannot apply to a non-open project.")

        # check duplicate
        existing = await self.proposal_repo.get_by_project_and_freelancer(project_id, freelancer_id)
        if existing:
            self.logger.warning(f"Duplicate proposal: freelancer={freelancer_id}, project={project_id}")
            raise ProposalAlreadyExists("You have already sent a proposal to this project.")

        proposal = Proposal.create(
            project_id=project_id,
            freelancer_id=freelancer_id,
            message=message,
            price=price,
            estimated_days=estimated_days
        )

        await self.proposal_repo.create(proposal)
        self.logger.info(f"Proposal created: {proposal}")

        await self.kafka_producer.send(
            topic=KAFKA_TOPICS["proposal_created"],
            event={
                "proposal_id": str(proposal.id),
                "project_id": str(proposal.project_id),
                "freelancer_id": str(proposal.freelancer_id),
                "status": proposal.status.value,
                "timestamp": datetime.now().isoformat()
            }
        )

        return proposal

    async def update_status(self, proposal_id: UUID, new_status: ProposalStatus) -> Proposal:
        proposal = await self.proposal_repo.get_by_id(proposal_id)
        if not proposal:
            raise ProposalNotFound(f"Proposal {proposal_id} not found")

        proposal.update_status(new_status)
        await self.proposal_repo.update(proposal)
        self.logger.info(f"Proposal status updated: {proposal.id} -> {new_status.value}")

        await self.kafka_producer.send(
            topic=KAFKA_TOPICS["proposal_updated"],
            event={
                "proposal_id": str(proposal.id),
                "freelancer_id": str(proposal.freelancer_id),
                "new_status": new_status.value,
                "timestamp": datetime.now().isoformat()
            }
        )

        return proposal

    async def get_by_id(self, proposal_id: UUID) -> Proposal:
        proposal = await self.proposal_repo.get_by_id(proposal_id)
        if not proposal:
            raise ProposalNotFound(f"Proposal {proposal_id} not found")
        return proposal

    async def list_by_project(self, project_id: UUID) -> list[Proposal]:
        return await self.proposal_repo.list_by_project(project_id)
