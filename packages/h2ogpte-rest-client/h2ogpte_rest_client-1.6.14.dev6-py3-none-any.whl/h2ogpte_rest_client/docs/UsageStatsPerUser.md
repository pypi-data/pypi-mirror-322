# UsageStatsPerUser


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **str** |  | 
**username** | **str** |  | 
**email** | **str** |  | 
**llm_usage** | [**List[UsageStatsPerModel]**](UsageStatsPerModel.md) |  | 

## Example

```python
from h2ogpte_rest_client.models.usage_stats_per_user import UsageStatsPerUser

# TODO update the JSON string below
json = "{}"
# create an instance of UsageStatsPerUser from a JSON string
usage_stats_per_user_instance = UsageStatsPerUser.from_json(json)
# print the JSON string representation of the object
print(UsageStatsPerUser.to_json())

# convert the object into a dict
usage_stats_per_user_dict = usage_stats_per_user_instance.to_dict()
# create an instance of UsageStatsPerUser from a dict
usage_stats_per_user_from_dict = UsageStatsPerUser.from_dict(usage_stats_per_user_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


