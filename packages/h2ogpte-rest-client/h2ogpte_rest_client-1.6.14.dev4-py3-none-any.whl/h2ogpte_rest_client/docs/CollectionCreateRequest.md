# CollectionCreateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | 
**embedding_model** | **str** |  | [optional] 
**collection_settings** | [**CollectionSettings**](CollectionSettings.md) |  | [optional] 
**chat_settings** | [**ChatSettings**](ChatSettings.md) |  | [optional] 

## Example

```python
from h2ogpte_rest_client.models.collection_create_request import CollectionCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CollectionCreateRequest from a JSON string
collection_create_request_instance = CollectionCreateRequest.from_json(json)
# print the JSON string representation of the object
print(CollectionCreateRequest.to_json())

# convert the object into a dict
collection_create_request_dict = collection_create_request_instance.to_dict()
# create an instance of CollectionCreateRequest from a dict
collection_create_request_from_dict = CollectionCreateRequest.from_dict(collection_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


