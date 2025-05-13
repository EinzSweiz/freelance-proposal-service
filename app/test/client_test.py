import grpc
from app.generated.project import project_pb2, project_pb2_grpc

def main():
    # Подключение к gRPC серверу (указываем имя контейнера, не localhost!)
    channel = grpc.insecure_channel("localhost:50051")
    stub = project_pb2_grpc.ProjectServiceStub(channel)

    request = project_pb2.GetProjectRequest(
        project_id="8ccbd150-3eb1-45d3-980e-33894399dd43"
    )

    try:
        response = stub.GetProjectById(request)
        print("✅ Получен ответ от gRPC сервера:")
        print(f"Project ID: {response.project_id}")
        print(f"Client ID: {response.client_id}")
        print(f"Status: {response.status}")
    except grpc.RpcError as e:
        print(f"❌ Ошибка: {e.code()} - {e.details()}")

if __name__ == "__main__":
    main()
