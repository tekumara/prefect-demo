FROM prefecthq/prefect:2.18.0-python3.10

# explicitly specify workdir expected by the deployment (even though its the same as the base image)
WORKDIR /opt/prefect

# install python dependencies
# dask dependences are needed by dask_kubes_flow
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e '.[dask]'

# point fsspec (ie: s3fs) at minio inside the cluster
COPY config/fsspec-minio.json config/fsspec.json
ENV FSSPEC_CONFIG_DIR=/opt/prefect/config

# add flows so they can be used by deployments with no storage
COPY flows flows
