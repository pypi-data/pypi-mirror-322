# UsageStatsPerModelAndUser


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**llm_name** | **str** |  | 
**total_cost** | **float** |  | 
**total_calls** | **int** |  | 
**total_input_tokens** | **int** |  | 
**total_output_tokens** | **int** |  | 
**user_usage** | [**List[ModelUsageStatsPerUser]**](ModelUsageStatsPerUser.md) |  | 

## Example

```python
from h2ogpte_rest_client.models.usage_stats_per_model_and_user import UsageStatsPerModelAndUser

# TODO update the JSON string below
json = "{}"
# create an instance of UsageStatsPerModelAndUser from a JSON string
usage_stats_per_model_and_user_instance = UsageStatsPerModelAndUser.from_json(json)
# print the JSON string representation of the object
print(UsageStatsPerModelAndUser.to_json())

# convert the object into a dict
usage_stats_per_model_and_user_dict = usage_stats_per_model_and_user_instance.to_dict()
# create an instance of UsageStatsPerModelAndUser from a dict
usage_stats_per_model_and_user_from_dict = UsageStatsPerModelAndUser.from_dict(usage_stats_per_model_and_user_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


