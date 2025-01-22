# ChatMessageMeta


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message_type** | **str** |  | 
**content** | **str** |  | 

## Example

```python
from h2ogpte_rest_client.models.chat_message_meta import ChatMessageMeta

# TODO update the JSON string below
json = "{}"
# create an instance of ChatMessageMeta from a JSON string
chat_message_meta_instance = ChatMessageMeta.from_json(json)
# print the JSON string representation of the object
print(ChatMessageMeta.to_json())

# convert the object into a dict
chat_message_meta_dict = chat_message_meta_instance.to_dict()
# create an instance of ChatMessageMeta from a dict
chat_message_meta_from_dict = ChatMessageMeta.from_dict(chat_message_meta_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


