# ModelUsageStatsPerUser


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **str** |  | 
**username** | **str** |  | 
**email** | **str** |  | 
**llm_cost** | **float** |  | 
**call_count** | **int** |  | 
**input_tokens** | **int** |  | 
**output_tokens** | **int** |  | 

## Example

```python
from h2ogpte_rest_client.models.model_usage_stats_per_user import ModelUsageStatsPerUser

# TODO update the JSON string below
json = "{}"
# create an instance of ModelUsageStatsPerUser from a JSON string
model_usage_stats_per_user_instance = ModelUsageStatsPerUser.from_json(json)
# print the JSON string representation of the object
print(ModelUsageStatsPerUser.to_json())

# convert the object into a dict
model_usage_stats_per_user_dict = model_usage_stats_per_user_instance.to_dict()
# create an instance of ModelUsageStatsPerUser from a dict
model_usage_stats_per_user_from_dict = ModelUsageStatsPerUser.from_dict(model_usage_stats_per_user_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


