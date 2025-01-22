# SuggestedQuestion


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**question** | **str** |  | 

## Example

```python
from h2ogpte_rest_client.models.suggested_question import SuggestedQuestion

# TODO update the JSON string below
json = "{}"
# create an instance of SuggestedQuestion from a JSON string
suggested_question_instance = SuggestedQuestion.from_json(json)
# print the JSON string representation of the object
print(SuggestedQuestion.to_json())

# convert the object into a dict
suggested_question_dict = suggested_question_instance.to_dict()
# create an instance of SuggestedQuestion from a dict
suggested_question_from_dict = SuggestedQuestion.from_dict(suggested_question_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


