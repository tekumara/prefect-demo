FROM prefecthq/prefect:2.0b8-python3.9

RUN pip install s3fs

# point fsspec at minio inside the cluster
COPY config/fsspec-minio.json config/fsspec.json
ENV FSSPEC_CONFIG_DIR=/opt/prefect/config
