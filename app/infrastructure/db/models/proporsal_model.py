import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import uuid4
from datetime import datetime
from enum import Enum

from app.infrastructure.db.db_session import Base


class ProposalStatusEnum(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class ProposalModel(Base):
    __tablename__ = "proposals"

    id = sa.Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = sa.Column(PG_UUID(as_uuid=True), nullable=False, index=True)
    freelancer_id = sa.Column(PG_UUID(as_uuid=True), nullable=False, index=True)
    message = sa.Column(sa.Text, nullable=False)
    price = sa.Column(sa.Float, nullable=False)
    estimated_days = sa.Column(sa.Integer, nullable=False)
    status = sa.Column(sa.Enum(ProposalStatusEnum), nullable=False, default=ProposalStatusEnum.PENDING)
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
    updated_at = sa.Column(sa.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
