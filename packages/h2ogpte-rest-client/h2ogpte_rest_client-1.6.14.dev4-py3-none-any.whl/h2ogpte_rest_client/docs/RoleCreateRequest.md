# RoleCreateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | 

## Example

```python
from h2ogpte_rest_client.models.role_create_request import RoleCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RoleCreateRequest from a JSON string
role_create_request_instance = RoleCreateRequest.from_json(json)
# print the JSON string representation of the object
print(RoleCreateRequest.to_json())

# convert the object into a dict
role_create_request_dict = role_create_request_instance.to_dict()
# create an instance of RoleCreateRequest from a dict
role_create_request_from_dict = RoleCreateRequest.from_dict(role_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


