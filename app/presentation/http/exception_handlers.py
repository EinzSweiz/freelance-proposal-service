from fastapi import Request
from fastapi.responses import JSONResponse

# Proposal exceptions
from app.domain.exceptions import (
    ProposalNotFound,
    ProposalAlreadyExists,
    ProjectNotOpen,
    UnauthorizedProposalAccess,
    ProposalAlreadyAccepted,
)


# --- Proposal Handlers ---

async def proposal_not_found(request: Request, exc: ProposalNotFound):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

async def proposal_already_exists(request: Request, exc: ProposalAlreadyExists):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

async def project_not_open(request: Request, exc: ProjectNotOpen):
    return JSONResponse(status_code=400, content={"detail": str(exc)})

async def unauthorized_proposal_access(request: Request, exc: UnauthorizedProposalAccess):
    return JSONResponse(status_code=403, content={"detail": str(exc)})

async def proposal_already_accepted(request: Request, exc: ProposalAlreadyAccepted):
    return JSONResponse(status_code=409, content={"detail": str(exc)})
