# IngestFromS3Request


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**urls** | **List[str]** | The path or list of paths of S3 files or directories. | 
**region** | **str** | The name of the region used for interaction with AWS services. | [optional] [default to 'us-east-1']
**credentials** | [**S3Credentials**](S3Credentials.md) |  | [optional] 

## Example

```python
from h2ogpte_rest_client.models.ingest_from_s3_request import IngestFromS3Request

# TODO update the JSON string below
json = "{}"
# create an instance of IngestFromS3Request from a JSON string
ingest_from_s3_request_instance = IngestFromS3Request.from_json(json)
# print the JSON string representation of the object
print(IngestFromS3Request.to_json())

# convert the object into a dict
ingest_from_s3_request_dict = ingest_from_s3_request_instance.to_dict()
# create an instance of IngestFromS3Request from a dict
ingest_from_s3_request_from_dict = IngestFromS3Request.from_dict(ingest_from_s3_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


