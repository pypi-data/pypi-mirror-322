# AzureCredentials

The object with Azure credentials. If container is private, set either `account_key` or `sas_token`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**account_key** | **str** |  | [optional] 
**sas_token** | **str** |  | [optional] 

## Example

```python
from h2ogpte_rest_client.models.azure_credentials import AzureCredentials

# TODO update the JSON string below
json = "{}"
# create an instance of AzureCredentials from a JSON string
azure_credentials_instance = AzureCredentials.from_json(json)
# print the JSON string representation of the object
print(AzureCredentials.to_json())

# convert the object into a dict
azure_credentials_dict = azure_credentials_instance.to_dict()
# create an instance of AzureCredentials from a dict
azure_credentials_from_dict = AzureCredentials.from_dict(azure_credentials_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


