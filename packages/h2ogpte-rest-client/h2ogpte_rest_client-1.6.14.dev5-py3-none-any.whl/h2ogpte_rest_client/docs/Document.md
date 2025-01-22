# Document


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | A unique identifier of the document | 
**name** | **str** | Name of the document | 
**type** | **str** | Type of the document | 
**size** | **int** | Size of the document in bytes | 
**updated_at** | **datetime** | Last time when document was modified | 
**uri** | **str** |  | [optional] 
**summary** | **str** |  | [optional] 
**summary_parameters** | **str** |  | [optional] 

## Example

```python
from h2ogpte_rest_client.models.document import Document

# TODO update the JSON string below
json = "{}"
# create an instance of Document from a JSON string
document_instance = Document.from_json(json)
# print the JSON string representation of the object
print(Document.to_json())

# convert the object into a dict
document_dict = document_instance.to_dict()
# create an instance of Document from a dict
document_from_dict = Document.from_dict(document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


