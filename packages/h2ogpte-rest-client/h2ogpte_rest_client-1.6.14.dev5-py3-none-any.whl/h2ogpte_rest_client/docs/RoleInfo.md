# RoleInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**name** | **str** |  | 
**description** | **str** |  | [optional] 

## Example

```python
from h2ogpte_rest_client.models.role_info import RoleInfo

# TODO update the JSON string below
json = "{}"
# create an instance of RoleInfo from a JSON string
role_info_instance = RoleInfo.from_json(json)
# print the JSON string representation of the object
print(RoleInfo.to_json())

# convert the object into a dict
role_info_dict = role_info_instance.to_dict()
# create an instance of RoleInfo from a dict
role_info_from_dict = RoleInfo.from_dict(role_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


