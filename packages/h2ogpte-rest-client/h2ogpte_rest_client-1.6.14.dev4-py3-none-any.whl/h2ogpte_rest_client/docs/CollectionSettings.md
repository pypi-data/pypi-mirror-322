# CollectionSettings


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**max_tokens_per_chunk** | **int** | Approximate max. number of tokens per chunk for text-dominated document pages. For images, chunks can be larger. | [optional] 
**chunk_overlap_tokens** | **int** | Approximate number of tokens that are overlapping between successive chunks. | [optional] 
**guardrails_settings** | [**GuardrailsSettings**](GuardrailsSettings.md) |  | [optional] 

## Example

```python
from h2ogpte_rest_client.models.collection_settings import CollectionSettings

# TODO update the JSON string below
json = "{}"
# create an instance of CollectionSettings from a JSON string
collection_settings_instance = CollectionSettings.from_json(json)
# print the JSON string representation of the object
print(CollectionSettings.to_json())

# convert the object into a dict
collection_settings_dict = collection_settings_instance.to_dict()
# create an instance of CollectionSettings from a dict
collection_settings_from_dict = CollectionSettings.from_dict(collection_settings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


