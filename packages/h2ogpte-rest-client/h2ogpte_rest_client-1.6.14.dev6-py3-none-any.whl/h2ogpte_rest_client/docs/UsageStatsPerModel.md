# UsageStatsPerModel


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**llm_name** | **str** |  | 
**llm_cost** | **float** |  | 
**call_count** | **int** |  | 
**input_tokens** | **int** |  | 
**output_tokens** | **int** |  | 

## Example

```python
from h2ogpte_rest_client.models.usage_stats_per_model import UsageStatsPerModel

# TODO update the JSON string below
json = "{}"
# create an instance of UsageStatsPerModel from a JSON string
usage_stats_per_model_instance = UsageStatsPerModel.from_json(json)
# print the JSON string representation of the object
print(UsageStatsPerModel.to_json())

# convert the object into a dict
usage_stats_per_model_dict = usage_stats_per_model_instance.to_dict()
# create an instance of UsageStatsPerModel from a dict
usage_stats_per_model_from_dict = UsageStatsPerModel.from_dict(usage_stats_per_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


