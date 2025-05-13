from fastapi import APIRouter, Depends, Request
from uuid import UUID
from typing import Annotated, List

from app.presentation.schemas.proporsal_schemas import (
    ProposalCreateRequest,
    ProposalUpdateStatusRequest,
    ProposalResponse,
    ProposalStatus,
)
from app.services.proporsal_service import ProposalService
from app.services.dependencies import get_proposal_service

router = APIRouter(prefix="/proposals", tags=["Proposals"])


@router.post("/", response_model=ProposalResponse)
async def create_proposal(
    request: Request,
    data: ProposalCreateRequest,
    service: Annotated[ProposalService, Depends(get_proposal_service)],
):
    user_id = request.state.user_id
    proposal = await service.create_proposal(
        project_id=data.project_id,
        freelancer_id=UUID(user_id),
        message=data.message,
        price=data.price,
        estimated_days=data.estimated_days,
    )
    return ProposalResponse(**proposal.to_dict())


@router.patch("/{proposal_id}", response_model=ProposalResponse)
async def update_proposal_status(
    proposal_id: UUID,
    data: ProposalUpdateStatusRequest,
    service: Annotated[ProposalService, Depends(get_proposal_service)],
):
    proposal = await service.update_status(proposal_id, data.status)
    return ProposalResponse(**proposal.to_dict())


@router.get("/{proposal_id}", response_model=ProposalResponse)
async def get_proposal_by_id(
    proposal_id: UUID,
    service: Annotated[ProposalService, Depends(get_proposal_service)],
):
    proposal = await service.get_by_id(proposal_id)
    return ProposalResponse(**proposal.to_dict())


@router.get("/project/{project_id}", response_model=List[ProposalResponse])
async def list_proposals_for_project(
    project_id: UUID,
    service: Annotated[ProposalService, Depends(get_proposal_service)],
):
    proposals = await service.list_by_project(project_id)
    return [ProposalResponse(**p.to_dict()) for p in proposals]
