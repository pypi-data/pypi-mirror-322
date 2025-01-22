# Collection


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | A unique identifier of the collection | 
**name** | **str** | Name of the collection | 
**description** | **str** | Description of the collection | 
**embedding_model** | **str** |  | 
**document_count** | **int** | A number of documents in the collection | 
**document_size** | **int** | Total size in bytes of all documents in the collection | 
**updated_at** | **datetime** | Last time when collection was modified | 
**user_count** | **int** | A number of users having access to the collection | 
**is_public** | **bool** | Is publicly accessible | 
**username** | **str** | Name of the user owning the collection | 
**sessions_count** | **int** | A number of chat sessions with the collection | 
**prompt_template_id** | **str** | A unique identifier of a prompt template associated with the collection. | [optional] 
**thumbnail** | **str** | A file name of a thumbnail image. | [optional] 

## Example

```python
from h2ogpte_rest_client.models.collection import Collection

# TODO update the JSON string below
json = "{}"
# create an instance of Collection from a JSON string
collection_instance = Collection.from_json(json)
# print the JSON string representation of the object
print(Collection.to_json())

# convert the object into a dict
collection_dict = collection_instance.to_dict()
# create an instance of Collection from a dict
collection_from_dict = Collection.from_dict(collection_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


