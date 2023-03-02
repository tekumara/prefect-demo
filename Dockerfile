FROM prefecthq/prefect:2.8.3-python3.9

# s3fs is used to fetch flows from minio
# dask dependences are needed by dask_kubes_flow
# bokeh is needed for the dask dashboard
RUN pip install --no-cache-dir bokeh==2.4.3 dask_kubernetes==2022.10.0 prefect-dask==0.2.1 s3fs==2022.8.2

# explictly specify workdir expected by the deployment (even though its the same as the base image)
WORKDIR /opt/prefect

# point fsspec at minio inside the cluster
COPY config/fsspec-minio.json config/fsspec.json
ENV FSSPEC_CONFIG_DIR=/opt/prefect/config

# add flows so they can be used by deployments with no storage
COPY flows flows
