# GuardrailsSettings


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**disallowed_regex_patterns** | **List[str]** | A list of regular expressions that match custom PII. | 
**presidio_labels_to_flag** | **List[str]** | A list of entities to be flagged as PII by the built-in Presidio model. | 
**pii_labels_to_flag** | **List[str]** | A list of entities to be flagged as PII by the built-in PII model. | 
**pii_detection_parse_action** | **str** | What to do when PII is detected during parsing of documents. The &#39;redact&#39; option will replace disallowed content in the ingested documents with redaction bars. | 
**pii_detection_llm_input_action** | **str** | What to do when PII is detected in the input to the LLM (document content and user prompts). The &#39;redact&#39; option will replace disallowed content with placeholders. | 
**pii_detection_llm_output_action** | **str** | What to do when PII is detected in the output of the LLM. The &#39;redact&#39; option will replace disallowed content with placeholders. | 
**prompt_guard_labels_to_flag** | **List[str]** | A list of entities to be flagged as safety violations in user prompts by the built-in prompt guard model. | 
**guardrails_labels_to_flag** | **List[str]** | A list of entities to be flagged as safety violations in user prompts. Must be a subset of guardrails_entities, if provided. | 
**guardrails_entities** | **Dict[str, str]** | Dictionary of entities and their descriptions for the guardrails model to classify. The first entry is the \&quot;safe\&quot; class, the rest are \&quot;unsafe\&quot; classes. | [optional] 

## Example

```python
from h2ogpte_rest_client.models.guardrails_settings import GuardrailsSettings

# TODO update the JSON string below
json = "{}"
# create an instance of GuardrailsSettings from a JSON string
guardrails_settings_instance = GuardrailsSettings.from_json(json)
# print the JSON string representation of the object
print(GuardrailsSettings.to_json())

# convert the object into a dict
guardrails_settings_dict = guardrails_settings_instance.to_dict()
# create an instance of GuardrailsSettings from a dict
guardrails_settings_from_dict = GuardrailsSettings.from_dict(guardrails_settings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


