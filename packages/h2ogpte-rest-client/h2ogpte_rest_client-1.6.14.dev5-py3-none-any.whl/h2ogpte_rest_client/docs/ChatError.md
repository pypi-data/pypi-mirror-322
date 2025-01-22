# ChatError


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error** | **str** |  | 

## Example

```python
from h2ogpte_rest_client.models.chat_error import ChatError

# TODO update the JSON string below
json = "{}"
# create an instance of ChatError from a JSON string
chat_error_instance = ChatError.from_json(json)
# print the JSON string representation of the object
print(ChatError.to_json())

# convert the object into a dict
chat_error_dict = chat_error_instance.to_dict()
# create an instance of ChatError from a dict
chat_error_from_dict = ChatError.from_dict(chat_error_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


