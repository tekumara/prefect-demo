from prefect import flow, get_run_logger
from prefect.deployments import DeploymentSpec
from prefect.flow_runners import KubernetesFlowRunner


@flow
def test_flow() -> None:
    # shown in kubectl logs but not prefect ui
    print("Hello from Kubernetes!")
    # show in prefect ui
    logger = get_run_logger()
    logger.info("Hello Prefect UI from Kubernetes!")


DeploymentSpec(
    flow=test_flow,
    name="test-deployment",
    flow_runner=KubernetesFlowRunner(stream_output=True),
)
