# GetCompletion200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**body** | **str** |  | 
**finished** | **bool** |  | 
**error** | **str** |  | 

## Example

```python
from h2ogpte_rest_client.models.get_completion200_response import GetCompletion200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetCompletion200Response from a JSON string
get_completion200_response_instance = GetCompletion200Response.from_json(json)
# print the JSON string representation of the object
print(GetCompletion200Response.to_json())

# convert the object into a dict
get_completion200_response_dict = get_completion200_response_instance.to_dict()
# create an instance of GetCompletion200Response from a dict
get_completion200_response_from_dict = GetCompletion200Response.from_dict(get_completion200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


