from prefect.filesystems import S3


def minio_flows() -> S3:
    name = "minio-flows"
    try:
        fs: S3 = S3.load(name)  # type: ignore
        print(f"Loaded S3 block '{fs.get_block_type_slug()}/{name}' (id {fs._block_document_id})")
        return fs
    except ValueError as e:
        if "Unable to find block document" in str(e):
            fs = S3(bucket_path="minio-flows")  # type: ignore
            doc_id = fs.save(name)

            print(f"Created S3 block '{name}' (id {doc_id})")
            return fs
        else:
            raise e
