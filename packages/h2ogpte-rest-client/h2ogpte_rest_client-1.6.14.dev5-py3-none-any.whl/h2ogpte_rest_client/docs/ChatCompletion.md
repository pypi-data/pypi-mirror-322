# ChatCompletion


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**body** | **str** |  | 

## Example

```python
from h2ogpte_rest_client.models.chat_completion import ChatCompletion

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletion from a JSON string
chat_completion_instance = ChatCompletion.from_json(json)
# print the JSON string representation of the object
print(ChatCompletion.to_json())

# convert the object into a dict
chat_completion_dict = chat_completion_instance.to_dict()
# create an instance of ChatCompletion from a dict
chat_completion_from_dict = ChatCompletion.from_dict(chat_completion_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


