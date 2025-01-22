# ChatSessionUpdateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 

## Example

```python
from h2ogpte_rest_client.models.chat_session_update_request import ChatSessionUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ChatSessionUpdateRequest from a JSON string
chat_session_update_request_instance = ChatSessionUpdateRequest.from_json(json)
# print the JSON string representation of the object
print(ChatSessionUpdateRequest.to_json())

# convert the object into a dict
chat_session_update_request_dict = chat_session_update_request_instance.to_dict()
# create an instance of ChatSessionUpdateRequest from a dict
chat_session_update_request_from_dict = ChatSessionUpdateRequest.from_dict(chat_session_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


