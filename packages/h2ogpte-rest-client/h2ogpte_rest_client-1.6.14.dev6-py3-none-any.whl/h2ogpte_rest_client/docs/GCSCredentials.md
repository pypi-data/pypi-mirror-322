# GCSCredentials

The object holding  JSON key of Google Cloud service account. If the object is not provided, only public buckets will be accessible.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**service_account_json_key** | **str** |  | 

## Example

```python
from h2ogpte_rest_client.models.gcs_credentials import GCSCredentials

# TODO update the JSON string below
json = "{}"
# create an instance of GCSCredentials from a JSON string
gcs_credentials_instance = GCSCredentials.from_json(json)
# print the JSON string representation of the object
print(GCSCredentials.to_json())

# convert the object into a dict
gcs_credentials_dict = gcs_credentials_instance.to_dict()
# create an instance of GCSCredentials from a dict
gcs_credentials_from_dict = GCSCredentials.from_dict(gcs_credentials_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


