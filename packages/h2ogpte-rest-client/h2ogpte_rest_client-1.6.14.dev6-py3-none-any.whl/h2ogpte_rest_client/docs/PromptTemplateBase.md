# PromptTemplateBase


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | A name of the prompt template. | [optional] 
**description** | **str** | A description of the prompt template. | [optional] 
**lang** | **str** | A language code. | [optional] 
**system_prompt** | **str** | A system prompt. | [optional] 
**pre_prompt_query** | **str** | A text that is prepended before the contextual document chunks. | [optional] 
**prompt_query** | **str** | A text that is appended to the beginning of the user&#39;s message. | [optional] 
**hyde_no_rag_llm_prompt_extension** | **str** | An LLM prompt extension. | [optional] 
**pre_prompt_summary** | **str** | A prompt that goes before each large piece of text to summarize. | [optional] 
**prompt_summary** | **str** | A prompt that goes after each large piece of text to summarize. | [optional] 
**system_prompt_reflection** | **str** | A system prompt for self-reflection. | [optional] 
**prompt_reflection** | **str** | A template for self-reflection, must contain two occurrences of %s for full previous prompt (including system prompt, document related context and prompts if applicable, and user prompts) and answer | [optional] 
**auto_gen_description_prompt** | **str** | A prompt to create a description of the collection. | [optional] 
**auto_gen_document_summary_pre_prompt_summary** | **str** | A &#x60;pre_prompt_summary&#x60; for summary of a freshly imported document (if enabled). | [optional] 
**auto_gen_document_summary_prompt_summary** | **str** | A &#x60;prompt_summary&#x60; for summary of a freshly imported document (if enabled).&#x60; | [optional] 
**auto_gen_document_sample_questions_prompt** | **str** | A prompt to create sample questions for a freshly imported document (if enabled). | [optional] 
**default_sample_questions** | **List[str]** | Default sample questions in case there are no auto-generated sample questions. | [optional] 
**image_batch_image_prompt** | **str** | A prompt for each image batch for vision models. | [optional] 
**image_batch_final_prompt** | **str** | A prompt for each image batch for vision models. | [optional] 

## Example

```python
from h2ogpte_rest_client.models.prompt_template_base import PromptTemplateBase

# TODO update the JSON string below
json = "{}"
# create an instance of PromptTemplateBase from a JSON string
prompt_template_base_instance = PromptTemplateBase.from_json(json)
# print the JSON string representation of the object
print(PromptTemplateBase.to_json())

# convert the object into a dict
prompt_template_base_dict = prompt_template_base_instance.to_dict()
# create an instance of PromptTemplateBase from a dict
prompt_template_base_from_dict = PromptTemplateBase.from_dict(prompt_template_base_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


