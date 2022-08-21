from prefect.filesystems import S3


def minio_flows_increment() -> S3:
    name = "minio-flows-increment"
    try:
        fs: S3 = S3.load(name)  # type: ignore
        print(f"{fs.get_block_type_slug()}/{name} has document id {fs._block_document_id}")
        return fs
    except ValueError as e:
        if "Unable to find block document" in str(e):
            fs = S3(bucket_path="minio-flows/increment")  # type: ignore
            doc_id = fs.save(name)

            print(f"Saved S3 block {name} with document id {doc_id}")
            return fs
        else:
            raise e
