# CollectionChangeRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**collection_id** | **str** |  | 

## Example

```python
from h2ogpte_rest_client.models.collection_change_request import CollectionChangeRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CollectionChangeRequest from a JSON string
collection_change_request_instance = CollectionChangeRequest.from_json(json)
# print the JSON string representation of the object
print(CollectionChangeRequest.to_json())

# convert the object into a dict
collection_change_request_dict = collection_change_request_instance.to_dict()
# create an instance of CollectionChangeRequest from a dict
collection_change_request_from_dict = CollectionChangeRequest.from_dict(collection_change_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


