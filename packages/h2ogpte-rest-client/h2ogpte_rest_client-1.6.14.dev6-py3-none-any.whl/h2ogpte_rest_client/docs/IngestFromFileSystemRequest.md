# IngestFromFileSystemRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**root_dir** | **str** | String path of where to look for files. | 
**glob** | **str** | String of the glob pattern used to match files in the root directory. | 

## Example

```python
from h2ogpte_rest_client.models.ingest_from_file_system_request import IngestFromFileSystemRequest

# TODO update the JSON string below
json = "{}"
# create an instance of IngestFromFileSystemRequest from a JSON string
ingest_from_file_system_request_instance = IngestFromFileSystemRequest.from_json(json)
# print the JSON string representation of the object
print(IngestFromFileSystemRequest.to_json())

# convert the object into a dict
ingest_from_file_system_request_dict = ingest_from_file_system_request_instance.to_dict()
# create an instance of IngestFromFileSystemRequest from a dict
ingest_from_file_system_request_from_dict = IngestFromFileSystemRequest.from_dict(ingest_from_file_system_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


