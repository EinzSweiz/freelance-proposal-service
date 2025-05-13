from dataclasses import dataclass
from enum import Enum
from uuid import uuid4, UUID
from datetime import datetime
from typing import Optional


class ProposalStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


@dataclass
class Proposal:
    id: UUID
    project_id: UUID
    freelancer_id: UUID
    message: str
    price: float
    estimated_days: int
    status: ProposalStatus
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at)
        if isinstance(self.updated_at, str):
            self.updated_at = datetime.fromisoformat(self.updated_at)

    @classmethod
    def create(
        cls,
        project_id: UUID,
        freelancer_id: UUID,
        message: str,
        price: float,
        estimated_days: int,
    ) -> "Proposal":
        now = datetime.now()
        return cls(
            id=uuid4(),
            project_id=project_id,
            freelancer_id=freelancer_id,
            message=message,
            price=price,
            estimated_days=estimated_days,
            status=ProposalStatus.PENDING,
            created_at=now,
            updated_at=now
        )

    def update_status(self, new_status: ProposalStatus):
        self.status = new_status
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "project_id": str(self.project_id),
            "freelancer_id": str(self.freelancer_id),
            "message": self.message,
            "price": self.price,
            "estimated_days": self.estimated_days,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Proposal":
        return cls(
            id=UUID(data["id"]),
            project_id=UUID(data["project_id"]),
            freelancer_id=UUID(data["freelancer_id"]),
            message=data["message"],
            price=float(data["price"]),
            estimated_days=int(data["estimated_days"]),
            status=ProposalStatus(data["status"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )
