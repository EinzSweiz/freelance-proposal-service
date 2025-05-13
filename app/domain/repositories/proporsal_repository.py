from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional
from app.domain.entities.proporsal_entity import Proposal


class AbstractProposalRepository(ABC):
    @abstractmethod
    async def create(self, proposal: Proposal) -> None:
        """Save a new proposal to the database."""
        pass

    @abstractmethod
    async def get_by_id(self, proposal_id: UUID) -> Optional[Proposal]:
        """Get a proposal by its ID."""
        pass

    @abstractmethod
    async def get_by_project_and_freelancer(self, project_id: UUID, freelancer_id: UUID) -> Optional[Proposal]:
        """Check if freelancer has already applied to the project."""
        pass

    @abstractmethod
    async def list_by_project(self, project_id: UUID) -> List[Proposal]:
        """List all proposals for a given project."""
        pass

    @abstractmethod
    async def update(self, proposal: Proposal) -> None:
        """Update proposal (e.g. change status)."""
        pass
