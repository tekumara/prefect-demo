from prefect.deployments import Deployment
from prefect.filesystems import RemoteFileSystem
from prefect.flow_runners import KubernetesFlowRunner
from prefect.packaging.file import FilePackager
from prefect.packaging.orion import OrionPackager
from prefect.packaging.serializers import ImportSerializer

from flows.kubes_flow import kubes_flow

# use the default packager (OrionPackager) to store the flow's source file
# as an anonymous JSON block in the Orion database. The block is encrypted.
Deployment(
    name="orion-packager",
    flow=kubes_flow,
    flow_runner=KubernetesFlowRunner(
        image="orion-registry:5000/flow:latest",
    ),
)

# use the OrionPackager with the ImportSerializer to store the flow's import path
# as a JSON block in the database, for import at runtime. Requires the flow be
# baked into the the docker image.
Deployment(
    name="orion-packager-import",
    flow=kubes_flow,
    flow_runner=KubernetesFlowRunner(
        image="orion-registry:5000/flow:latest",
    ),
    packager=OrionPackager(serializer=ImportSerializer()),
)

# use the FilePackager to store the flow's source file in S3 using fsspec
Deployment(
    name="file-packager",
    flow=kubes_flow,
    flow_runner=KubernetesFlowRunner(
        image="orion-registry:5000/flow:latest",
        # use to read the stored flow from minio when the flow executes
        env={"AWS_ACCESS_KEY_ID": "minioadmin", "AWS_SECRET_ACCESS_KEY": "minioadmin"},
    ),
    packager=FilePackager(filesystem=RemoteFileSystem(basepath="s3://minio-flows/")),
)
