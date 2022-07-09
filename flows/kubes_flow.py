from prefect import flow, get_run_logger
from prefect.deployments import Deployment
from prefect.filesystems import RemoteFileSystem
from prefect.flow_runners import KubernetesFlowRunner
from prefect.packaging.file import FilePackager
from prefect.packaging.orion import OrionPackager
from prefect.packaging.serializers import ImportSerializer


@flow
def kubes_flow() -> None:
    # shown in kubectl logs but not prefect ui
    print("Hello from Kubernetes!")
    # show in prefect ui
    logger = get_run_logger()
    logger.info("Hello Prefect UI from Kubernetes!")


# use the default packager (OrionPackager) to store the flow's source file
# as an anonymous JSON block in the Orion database. The block is encrypted.
Deployment(
    name="kubes-deployment-orion-packager",
    flow=kubes_flow,
    flow_runner=KubernetesFlowRunner(
        image="orion-registry:5000/flow:latest",
    ),
)

# use the FilePackager to store the flow's source file in S3
Deployment(
    name="kubes-deployment-file-packager",
    flow=kubes_flow,
    flow_runner=KubernetesFlowRunner(
        image="orion-registry:5000/flow:latest",
        # use to read the stored flow from minio when the flow executes
        env={"AWS_ACCESS_KEY_ID": "minioadmin", "AWS_SECRET_ACCESS_KEY": "minioadmin"},
    ),
    packager=FilePackager(filesystem=RemoteFileSystem(basepath="s3://minio-flows/")),
)

# use the default OrionPackager to store the flow's import path as a block in the database.
# The flow is already stored inside the docker image and so can be imported.
Deployment(
    name="kubes-deployment-orion-packager-import",
    flow=kubes_flow,
    flow_runner=KubernetesFlowRunner(
        image="orion-registry:5000/flow:latest",
    ),
    packager=OrionPackager(serializer=ImportSerializer()),
)
