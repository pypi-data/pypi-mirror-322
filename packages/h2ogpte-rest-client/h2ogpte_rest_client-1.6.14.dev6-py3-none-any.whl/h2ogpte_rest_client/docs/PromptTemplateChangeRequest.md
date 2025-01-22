# PromptTemplateChangeRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prompt_template_id** | **str** |  | [optional] 

## Example

```python
from h2ogpte_rest_client.models.prompt_template_change_request import PromptTemplateChangeRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PromptTemplateChangeRequest from a JSON string
prompt_template_change_request_instance = PromptTemplateChangeRequest.from_json(json)
# print the JSON string representation of the object
print(PromptTemplateChangeRequest.to_json())

# convert the object into a dict
prompt_template_change_request_dict = prompt_template_change_request_instance.to_dict()
# create an instance of PromptTemplateChangeRequest from a dict
prompt_template_change_request_from_dict = PromptTemplateChangeRequest.from_dict(prompt_template_change_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


