# TagCreateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 

## Example

```python
from h2ogpte_rest_client.models.tag_create_request import TagCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TagCreateRequest from a JSON string
tag_create_request_instance = TagCreateRequest.from_json(json)
# print the JSON string representation of the object
print(TagCreateRequest.to_json())

# convert the object into a dict
tag_create_request_dict = tag_create_request_instance.to_dict()
# create an instance of TagCreateRequest from a dict
tag_create_request_from_dict = TagCreateRequest.from_dict(tag_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


