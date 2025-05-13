# app/infrastructure/grpc/project_client.py

import grpc
import os
from app.generated.proporsal import proporsal_pb2, proporsal_pb2_grpc

PROJECT_GRPC_HOST = os.getenv("PROJECT_GRPC_HOST", "grpc_server")
PROJECT_GRPC_PORT = os.getenv("PROJECT_GRPC_PORT", "50051")


class ProjectServiceClient:
    def __init__(self):
        self.channel = None
        self.stub = None

    async def init(self):
        self.channel = grpc.aio.insecure_channel(f"{PROJECT_GRPC_HOST}:{PROJECT_GRPC_PORT}")
        self.stub = proporsal_pb2_grpc.ProjectServiceStub(self.channel)

    async def get_project_by_id(self, project_id: str) -> dict:
        if self.stub is None:
            await self.init()

        request = proporsal_pb2.GetProjectRequest(project_id=str(project_id))
        response = await self.stub.GetProjectById(request)
        return {
            "project_id": response.project_id,
            "client_id": response.client_id,
            "status": response.status,
        }
