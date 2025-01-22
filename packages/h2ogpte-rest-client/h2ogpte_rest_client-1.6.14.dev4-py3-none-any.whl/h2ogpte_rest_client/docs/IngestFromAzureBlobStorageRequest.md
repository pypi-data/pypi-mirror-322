# IngestFromAzureBlobStorageRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**container** | **str** | Name of the Azure Blob Storage container. | 
**paths** | **List[str]** | Path or list of paths to files or directories within an Azure Blob Storage container. | 
**account_name** | **str** | Name of a storage account | 
**credentials** | [**AzureCredentials**](AzureCredentials.md) |  | [optional] 

## Example

```python
from h2ogpte_rest_client.models.ingest_from_azure_blob_storage_request import IngestFromAzureBlobStorageRequest

# TODO update the JSON string below
json = "{}"
# create an instance of IngestFromAzureBlobStorageRequest from a JSON string
ingest_from_azure_blob_storage_request_instance = IngestFromAzureBlobStorageRequest.from_json(json)
# print the JSON string representation of the object
print(IngestFromAzureBlobStorageRequest.to_json())

# convert the object into a dict
ingest_from_azure_blob_storage_request_dict = ingest_from_azure_blob_storage_request_instance.to_dict()
# create an instance of IngestFromAzureBlobStorageRequest from a dict
ingest_from_azure_blob_storage_request_from_dict = IngestFromAzureBlobStorageRequest.from_dict(ingest_from_azure_blob_storage_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


