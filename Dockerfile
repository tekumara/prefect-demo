FROM prefecthq/prefect:2.10.20-python3.10

# s3fs is used to fetch flows from minio
# dask dependences are needed by dask_kubes_flow
# bokeh is needed for the dask dashboard
RUN pip install --no-cache-dir bokeh==2.4.3 dask_kubernetes==2023.6.1 prefect-dask==0.2.4 s3fs==2023.6.0

# explicitly specify workdir expected by the deployment (even though its the same as the base image)
WORKDIR /opt/prefect

# point fsspec at minio inside the cluster
COPY config/fsspec-minio.json config/fsspec.json
ENV FSSPEC_CONFIG_DIR=/opt/prefect/config

# add flows so they can be used by deployments with no storage
COPY flows flows
