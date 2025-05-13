from uuid import UUID
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.domain.entities.proporsal_entity import Proposal, ProposalStatus
from app.domain.repositories.proporsal_repository import AbstractProposalRepository
from app.domain.common.logger import AbstractLogger
from app.infrastructure.db.models.proporsal_model import ProposalModel, ProposalStatusEnum


class PostgresqlProposalRepository(AbstractProposalRepository):
    def __init__(self, session: AsyncSession, logger: AbstractLogger) -> None:
        self.session = session
        self.logger = logger

    async def create(self, proposal: Proposal) -> None:
        self.logger.debug(f"Creating proposal: {proposal}")
        db_proposal = ProposalModel(
            id=proposal.id,
            project_id=proposal.project_id,
            freelancer_id=proposal.freelancer_id,
            message=proposal.message,
            price=proposal.price,
            estimated_days=proposal.estimated_days,
            status=ProposalStatusEnum(proposal.status.value),
            created_at=proposal.created_at,
            updated_at=proposal.updated_at
        )
        self.session.add(db_proposal)
        await self.session.commit()
        self.logger.info(f"Proposal created with ID: {proposal.id}")

    async def get_by_id(self, proposal_id: UUID) -> Optional[Proposal]:
        self.logger.debug(f"Fetching proposal by ID: {proposal_id}")
        result = await self.session.execute(
            select(ProposalModel).where(ProposalModel.id == proposal_id)
        )
        record = result.scalar_one_or_none()
        if record:
            self.logger.info(f"Proposal found with ID: {proposal_id}")
        else:
            self.logger.warning(f"Proposal not found with ID: {proposal_id}")
        return self._to_entity(record) if record else None

    async def get_by_project_and_freelancer(self, project_id: UUID, freelancer_id: UUID) -> Optional[Proposal]:
        self.logger.debug(f"Checking proposal by project_id={project_id}, freelancer_id={freelancer_id}")
        result = await self.session.execute(
            select(ProposalModel).where(
                ProposalModel.project_id == project_id,
                ProposalModel.freelancer_id == freelancer_id
            )
        )
        record = result.scalar_one_or_none()
        return self._to_entity(record) if record else None

    async def list_by_project(self, project_id: UUID) -> List[Proposal]:
        self.logger.debug(f"Listing proposals for project_id: {project_id}")
        result = await self.session.execute(
            select(ProposalModel).where(ProposalModel.project_id == project_id)
        )
        records = result.scalars().all()
        return [self._to_entity(r) for r in records]

    async def update(self, proposal: Proposal) -> None:
        self.logger.debug(f"Updating proposal with ID: {proposal.id}")
        result = await self.session.execute(
            select(ProposalModel).where(ProposalModel.id == proposal.id)
        )
        db_proposal = result.scalar_one_or_none()
        if not db_proposal:
            self.logger.warning(f"Proposal not found for update: {proposal.id}")
            return

        db_proposal.status = ProposalStatusEnum(proposal.status.value)
        db_proposal.updated_at = proposal.updated_at
        await self.session.commit()
        self.logger.info(f"Proposal updated with ID: {proposal.id}")

    def _to_entity(self, model: ProposalModel) -> Proposal:
        return Proposal(
            id=model.id,
            project_id=model.project_id,
            freelancer_id=model.freelancer_id,
            message=model.message,
            price=model.price,
            estimated_days=model.estimated_days,
            status=ProposalStatus(model.status.value),
            created_at=model.created_at,
            updated_at=model.updated_at
        )
