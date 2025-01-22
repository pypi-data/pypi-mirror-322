# PerformanceStatsPerModel


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**llm_name** | **str** |  | 
**call_count** | **int** |  | 
**input_tokens** | **int** |  | 
**output_tokens** | **int** |  | 
**tokens_per_second** | **float** |  | 
**time_to_first_token** | **float** |  | 

## Example

```python
from h2ogpte_rest_client.models.performance_stats_per_model import PerformanceStatsPerModel

# TODO update the JSON string below
json = "{}"
# create an instance of PerformanceStatsPerModel from a JSON string
performance_stats_per_model_instance = PerformanceStatsPerModel.from_json(json)
# print the JSON string representation of the object
print(PerformanceStatsPerModel.to_json())

# convert the object into a dict
performance_stats_per_model_dict = performance_stats_per_model_instance.to_dict()
# create an instance of PerformanceStatsPerModel from a dict
performance_stats_per_model_from_dict = PerformanceStatsPerModel.from_dict(performance_stats_per_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


