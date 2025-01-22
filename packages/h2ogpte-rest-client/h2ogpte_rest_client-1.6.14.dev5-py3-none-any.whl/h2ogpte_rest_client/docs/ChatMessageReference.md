# ChatMessageReference


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**collection_id** | **str** |  | [optional] 
**document_id** | **str** |  | 
**document_name** | **str** |  | 
**chunk_id** | **int** |  | 
**pages** | **str** |  | 
**content** | **str** |  | [optional] 
**were_references_deleted** | **bool** |  | 

## Example

```python
from h2ogpte_rest_client.models.chat_message_reference import ChatMessageReference

# TODO update the JSON string below
json = "{}"
# create an instance of ChatMessageReference from a JSON string
chat_message_reference_instance = ChatMessageReference.from_json(json)
# print the JSON string representation of the object
print(ChatMessageReference.to_json())

# convert the object into a dict
chat_message_reference_dict = chat_message_reference_instance.to_dict()
# create an instance of ChatMessageReference from a dict
chat_message_reference_from_dict = ChatMessageReference.from_dict(chat_message_reference_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


