# Blocks

[Blocks](https://docs.prefect.io/concepts/blocks/) are the core abstraction for storing configuration data in the server database, and the common interface for interacting with external systems that require configuration.

Blocks can be configured once and managed in a central location (the Prefect server). Flows can then reference this central configuration by name, similar to AWS Parameter Store. Unlike AWS Parameter Store, Blocks also provide a client-side SDK for interacting with an external system via that configuration. Prefect plans to use the Blocks abstraction to build out an SDK for interacting with all the tools in the modern data stack.

Block classes are pydantic models with arbitrary fields/methods and a common API for saving/loading them from the server API/database:

- [load](https://docs.prefect.io/api-ref/prefect/blocks/core/#prefect.blocks.core.Block.load) retrieves a named block from the server API/database.
- [save](https://docs.prefect.io/api-ref/prefect/blocks/core/#prefect.blocks.core.Block.save) saves a named block to the server API/database.

An instance of a block is stored as a block document with a name or without (aka an anonymous block).

Block classes include:

- JSON, DateTime, and String blocks
- EnvironmentVariable block that reads its value from an environment variable
- KubernetesClusterConfig
- Slack Webhook
- [Storage](https://docs.prefect.io/concepts/storage/)
- [File systems](https://docs.prefect.io/concepts/filesystems/)

## Example

RemoteFileSystem is a block, and so [configured RemoteFileSystem instances can be saved](https://docs.prefect.io/concepts/filesystems/#saving-and-loading-file-systems), eg:

```python
fs = RemoteFileSystem(basepath="s3://my-bucket/folder/")
fs.write_path("foo", b"hello")
fs.save("dev-s3")
```

To load:

```python
fs = RemoteFileSystem.load("dev-s3")
fs.read_path("foo")  # b'hello'
```

## UI

Named blocks can be [viewed and edited in the UI](http://localhost:4200/blocks). Anonymous blocks are not visible.

<img src="https://aws1.discourse-cdn.com/business7/uploads/prefecthq/original/2X/e/eacd71cdec026a0b16b170f37bda4e0ba9cce9f3.png" width="600"/>

## Database representation

Inpsect deployment package manifests:

```sql
select json_extract(flow_data,'$.blob') from deployment;
```

The OrionPackageManifest stores flow data as a block document:

```json
{
  "type": "orion",
  "flow_name": "kubes-flow",
  "flow_parameter_schema": {
    "title": "Parameters",
    "type": "object",
    "properties": {},
    "required": null,
    "definitions": null
  },
  "serializer": { "type": "source" },
  "block_document_id": "b61967e0-f665-41a4-84d1-cf06f5514f2c"
}
```

Blocks are [stored encrypted](https://github.com/PrefectHQ/prefect/blob/1d4dfa5055c46d7769c571b6a66aaec8e6cdfc13/src/prefect/orion/models/block_documents.py#L79) in the block_document table:

```sql
select * from block_document;
```

```
id|created|updated|name|data|block_schema_id|is_default_storage_block_document|block_type_id|is_anonymous
b61967e0-f665-41a4-84d1-cf06f5514f2c|2022-07-09 06:41:41.242948|2022-07-09 06:41:41.243058|anonymous:6e5336ad1712905d5ca107b432a50e99|"gAAAAABiySMl_NR-DYaDKhF-5Xeqhp_-sawtFJwyB3NE4oHxGrNwRo1JpWWS4dHAUtUn-9sLzFQtgGESZI-YcTyT0pYwGT_kSBBgE7Q67GiupwRLmhpZRaqPFzfF0h0-ozwL0vZPqS3OMqpMoWqN9XxOgMsHfwiwRxMhBqtZsRovAVusn8IdxsMt-SzaBASlE2O1tbrZuKbLvHCDFTuhvIGEZ2hEO8Uar6hOPcsw7w7GaOsydft10GaXVDlmYMPk9LwgyijxxnsLhRRMyCV3z0oOoQ8rwmgR-jhDAn0A1eVezeLMDlkuBCOzM5Ky-ngjLa2iFCzgaR_rcaRi7Jg9umLg-L7ZA8oUlKu-9YG0AyWrFgHZm20jZjNYzXLdcn6hzVJQ1kLikt4TyXuvo1Pzff2YAFdaxZfWI1bWADGAmTrJYVbV1uhFpBBEPO0E-iSIruHWhaXf7w9rETdmf5dQ1Nz1YjdB-3GKdwKatCiCpP2gVbBst9hVoFAFeptSZuriItwqbhtAGPhwyawUNRL40LcxMmSRbcxYosFuYcuNIVtmNB_YC3wSTFa--uB6weTYtZ_fWSc3_7Ll22fCKlm_qcbZ-TfxkQOcoBdfTOa42ARBi64wVH9OH-MTMawU955t2CJnCpd_Ou3HDy-fYccr30qfTTfeVKC_d4ODh6itQ8M0DYogTJz6H2U09S2PjcvYVsA9jn1qXMXr70RnGYs0YtACR19Sst8n_ZzMGT8qnHlCpY4fYQkXWQLNANtlY-PoZSJjruin8Lc7J9rXSVhN9k6ty1DfsfGmq5JT3v5U9S7eTTKj1bfflc4_1tJj1wW6Cx5eIWdT_aKGQMjO8ucbzKeQIZ6EDxdGxVaD_7_IILG-S1lmjZuj1eH5ExbVVJtDIv2azIqF4QaSjJrBsN1SoPUvLdjXgrs3bG7hzRtqntlzHxID0sRw7vA7oHYts_Y5cuRCYA-hzXaKNrQzaO-b9J7b5jwGlKcYJnSmBEB5Q6Xv_-dQBJDra48j3G4w5ILhAnPlciOQFiBt_CrHaE02dhxsRXkGDgD-b4HsRSADxt3lPkNtr94-1nyFJsnb-DECnyPNqmNJAQDaW9Bt60w-n-QqOwTAF87ZtXOTwFCjBfIswR4D6FYbEo4RDPgA3_YmHjVHI1QTSzLa5EFSKyHNystLh_WuKHSvs5LQ9XDAbfal437QSFWaFF7uK3D1afkqGeZSV3ooM9zPx8yN5DpV3lLout8gUVFQAzn2fIOoDBbdclVvIo4lzSw="|02afbc00-fc1e-4dd5-8d42-57b165376620|0|4dfbd6a2-ba1b-4b44-bfb3-c2732f9fe5dd|1
```

The encryption key is read from the [`ORION_ENCRYPTION_KEY` environment variable](https://github.com/PrefectHQ/prefect/blob/1d4dfa5055c46d7769c571b6a66aaec8e6cdfc13/src/prefect/orion/utilities/encryption.py#L15) if it exists, otherwise it's generated and stored in the `configuration` table in the database (alongside the same data that is being encrypted, which defeats the purpose!).

List block types:

```sql
select id,name,slug from block_type;
```

```
id|name|slug
88d49efe-c6da-4dab-ab10-d1d1ad12a439|Slack Webhook|slack-webhook
7d40d174-bade-4f19-9ae2-597a932b1d2d|JSON|json
2b0bf181-4651-4c9f-bbd2-40e2.8.37cf6|String|string
d214ce8c-9c28-438c-b19c-5c0c27ac4d60|Date Time|date-time
9b8d7f99-1cc0-4827-9ea4-b246a82ebd25|Secret|secret
3a30cb61-a343-4662-a032-3eefc2e3a65f|Local File System|local-file-system
c1564e32-ce3b-4258-83e5-482937707ec9|Remote File System|remote-file-system
022ff997-4b29-4721-8f99-196d63354555|S3|s3
8cdbd15b-897a-41fc-871c-871b7786ee29|GCS|gcs
57cb7e9f-073c-4583-92e1-a600fc482f65|Docker Container|docker-container
c9d25346-956c-46f1-b98a-94764cf2fef8|Kubernetes Cluster Config|kubernetes-cluster-config
507f55b8-c9ec-4cee-a0e6-0e2676bd641c|Kubernetes Job|kubernetes-job
36ced213-7003-4a8d-9fe8-af0d5dbf7eb3|Process|process
```

## API

The decrypted contents of the block document can be fetched from the API, together with the block_schema and block_type, eg:

```bash
curl "http://localhost:4200/api/block_documents/b61967e0-f665-41a4-84d1-cf06f5514f2c?include_secrets=true"
```

```json
{
  "id": "b61967e0-f665-41a4-84d1-cf06f5514f2c",
  "created": "2022-07-09T06:41:41.242948+00:00",
  "updated": "2022-07-09T06:41:41.243058+00:00",
  "name": "anonymous:6e5336ad1712905d5ca107b432a50e99",
  "data": {
    "value": {
      "flow": "{\"source\": \"from prefect import flow, get_run_logger\\nfrom prefect.blocks.storage import FileStorageBlock\\nfrom prefect.deployments import Deployment\\nfrom prefect.flow_runners import KubernetesFlowRunner\\n\\n\\n@flow\\ndef kubes_flow() -> None:\\n    # shown in kubectl logs but not prefect ui\\n    print(\\\"Hello from Kubernetes!\\\")\\n    # show in prefect ui\\n    logger = get_run_logger()\\n    logger.info(\\\"Hello Prefect UI from Kubernetes!\\\")\\n\\n\\nDeployment(\\n    name=\\\"kubes-deployment\\\",\\n    flow=kubes_flow,\\n    flow_runner=KubernetesFlowRunner(\\n        image=\\\"prefect-registry:5000/flow:latest\\\",\\n        stream_output=True,\\n        env={\\\"AWS_ACCESS_KEY_ID\\\": \\\"minioadmin\\\", \\\"AWS_SECRET_ACCESS_KEY\\\": \\\"minioadmin\\\"},\\n    )\\n)\\n\", \"file_name\": \"kubes_flow.py\", \"symbol_name\": \"kubes_flow\"}"
    }
  },
  "block_schema_id": "02afbc00-fc1e-4dd5-8d42-57b165376620",
  "block_schema": {
    "id": "02afbc00-fc1e-4dd5-8d42-57b165376620",
    "created": "2022-07-09T06:38:11.900676+00:00",
    "updated": "2022-07-09T06:41:41.126000+00:00",
    "checksum": "sha256:767ab2520040f319ca8d60e137cf23f9698fe51deb30b2b2f5848d0944a336d7",
    "fields": {
      "title": "JSON",
      "description": "A block that represents JSON",
      "type": "object",
      "properties": {
        "value": {
          "title": "Value",
          "description": "A JSON-compatible value"
        }
      },
      "required": ["value"],
      "block_type_name": "JSON",
      "secret_fields": [],
      "block_schema_references": {}
    },
    "block_type_id": "4dfbd6a2-ba1b-4b44-bfb3-c2732f9fe5dd",
    "block_type": {
      "id": "4dfbd6a2-ba1b-4b44-bfb3-c2732f9fe5dd",
      "created": "2022-07-09T06:38:11.722069+00:00",
      "updated": "2022-07-09T06:38:11.7222.8.30:00",
      "name": "JSON",
      "logo_url": null,
      "documentation_url": null,
      "description": null,
      "code_example": null,
      "is_protected": false
    },
    "capabilities": []
  },
  "block_type_id": "4dfbd6a2-ba1b-4b44-bfb3-c2732f9fe5dd",
  "block_type": {
    "id": "4dfbd6a2-ba1b-4b44-bfb3-c2732f9fe5dd",
    "created": "2022-07-09T06:38:11.722069+00:00",
    "updated": "2022-07-09T06:38:11.7222.8.30:00",
    "name": "JSON",
    "logo_url": null,
    "documentation_url": null,
    "description": null,
    "code_example": null,
    "is_protected": false
  },
  "block_document_references": {},
  "is_anonymous": true
}
```

## Reference

- [Concepts - Blocks](https://docs.prefect.io/concepts/blocks/)
