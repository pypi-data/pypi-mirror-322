# ChatMessage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**content** | **str** |  | 
**votes** | **int** |  | 
**created_at** | **datetime** |  | 
**has_references** | **bool** |  | 
**total_references** | **int** |  | 
**username** | **str** |  | [optional] 
**reply_to** | **str** |  | [optional] 
**error** | **str** |  | [optional] 
**type_list** | [**List[ChatMessageMeta]**](ChatMessageMeta.md) |  | [optional] 

## Example

```python
from h2ogpte_rest_client.models.chat_message import ChatMessage

# TODO update the JSON string below
json = "{}"
# create an instance of ChatMessage from a JSON string
chat_message_instance = ChatMessage.from_json(json)
# print the JSON string representation of the object
print(ChatMessage.to_json())

# convert the object into a dict
chat_message_dict = chat_message_instance.to_dict()
# create an instance of ChatMessage from a dict
chat_message_from_dict = ChatMessage.from_dict(chat_message_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


