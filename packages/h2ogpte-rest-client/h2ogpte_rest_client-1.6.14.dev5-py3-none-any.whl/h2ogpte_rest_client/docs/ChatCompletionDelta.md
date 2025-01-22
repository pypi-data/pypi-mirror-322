# ChatCompletionDelta


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**body** | **str** |  | 
**finished** | **bool** |  | 

## Example

```python
from h2ogpte_rest_client.models.chat_completion_delta import ChatCompletionDelta

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionDelta from a JSON string
chat_completion_delta_instance = ChatCompletionDelta.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionDelta.to_json())

# convert the object into a dict
chat_completion_delta_dict = chat_completion_delta_instance.to_dict()
# create an instance of ChatCompletionDelta from a dict
chat_completion_delta_from_dict = ChatCompletionDelta.from_dict(chat_completion_delta_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


