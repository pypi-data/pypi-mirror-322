# S3Credentials

The object with S3 credentials. If the object is not provided, only public buckets will be accessible.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**access_key_id** | **str** |  | 
**secret_access_key** | **str** |  | 
**session_token** | **str** |  | [optional] 
**role_arn** | **str** |  | [optional] 

## Example

```python
from h2ogpte_rest_client.models.s3_credentials import S3Credentials

# TODO update the JSON string below
json = "{}"
# create an instance of S3Credentials from a JSON string
s3_credentials_instance = S3Credentials.from_json(json)
# print the JSON string representation of the object
print(S3Credentials.to_json())

# convert the object into a dict
s3_credentials_dict = s3_credentials_instance.to_dict()
# create an instance of S3Credentials from a dict
s3_credentials_from_dict = S3Credentials.from_dict(s3_credentials_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


