class ProposalServiceException(Exception):
    """Base class for all proposal-related exceptions."""
    pass


class ProposalAlreadyExists(ProposalServiceException):
    """Raised when a freelancer already sent a proposal to this project."""
    pass


class ProposalNotFound(ProposalServiceException):
    """Raised when the requested proposal does not exist."""
    pass


class ProjectNotOpen(ProposalServiceException):
    """Raised when trying to apply to a project that is not open."""
    pass


class UnauthorizedProposalAccess(ProposalServiceException):
    """Raised when someone tries to modify a proposal they don't own."""
    pass


class ProposalAlreadyAccepted(ProposalServiceException):
    """Raised when a client tries to accept another proposal for the same project."""
    pass
