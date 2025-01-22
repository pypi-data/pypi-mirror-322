# IngestFromGcsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**urls** | **List[str]** | The path or list of paths of GCS files or directories. | 
**credentials** | [**GCSCredentials**](GCSCredentials.md) |  | [optional] 

## Example

```python
from h2ogpte_rest_client.models.ingest_from_gcs_request import IngestFromGcsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of IngestFromGcsRequest from a JSON string
ingest_from_gcs_request_instance = IngestFromGcsRequest.from_json(json)
# print the JSON string representation of the object
print(IngestFromGcsRequest.to_json())

# convert the object into a dict
ingest_from_gcs_request_dict = ingest_from_gcs_request_instance.to_dict()
# create an instance of IngestFromGcsRequest from a dict
ingest_from_gcs_request_from_dict = IngestFromGcsRequest.from_dict(ingest_from_gcs_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


