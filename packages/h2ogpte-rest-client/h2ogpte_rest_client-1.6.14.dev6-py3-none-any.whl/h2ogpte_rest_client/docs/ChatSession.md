# ChatSession


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**name** | **str** |  | [optional] 
**collection_id** | **str** |  | [optional] 
**prompt_template_id** | **str** |  | [optional] 
**latest_message_content** | **str** |  | [optional] 
**updated_at** | **datetime** |  | 

## Example

```python
from h2ogpte_rest_client.models.chat_session import ChatSession

# TODO update the JSON string below
json = "{}"
# create an instance of ChatSession from a JSON string
chat_session_instance = ChatSession.from_json(json)
# print the JSON string representation of the object
print(ChatSession.to_json())

# convert the object into a dict
chat_session_dict = chat_session_instance.to_dict()
# create an instance of ChatSession from a dict
chat_session_from_dict = ChatSession.from_dict(chat_session_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


