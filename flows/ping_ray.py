import grpc
import grpc._channel
import ray.core.generated.ray_client_pb2 as ray_client_pb2
import ray.core.generated.ray_client_pb2_grpc as ray_client_pb2_grpc


def ping() -> ray_client_pb2.ClusterInfoResponse:
    with grpc.insecure_channel("localhost:10001") as channel:
        stub = ray_client_pb2_grpc.RayletDriverStub(channel)
        return stub.ClusterInfo(ray_client_pb2.ClusterInfoRequest(type="PING"))


try:
    print(ping())
except grpc._channel._InactiveRpcError as e:
    print(f"{e.code()} {e.details()}")
    exit(42)
