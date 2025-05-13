from pydantic import BaseModel, Field
from uuid import UUID
from enum import Enum
from datetime import datetime


class ProposalStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class ProposalCreateRequest(BaseModel):
    project_id: UUID
    message: str = Field(..., min_length=5)
    price: float
    estimated_days: int


class ProposalUpdateStatusRequest(BaseModel):
    status: ProposalStatus


class ProposalResponse(BaseModel):
    id: UUID
    project_id: UUID
    freelancer_id: UUID
    message: str
    price: float
    estimated_days: int
    status: ProposalStatus
    created_at: datetime
    updated_at: datetime
