# UploadedFile


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**filename** | **str** |  | 

## Example

```python
from h2ogpte_rest_client.models.uploaded_file import UploadedFile

# TODO update the JSON string below
json = "{}"
# create an instance of UploadedFile from a JSON string
uploaded_file_instance = UploadedFile.from_json(json)
# print the JSON string representation of the object
print(UploadedFile.to_json())

# convert the object into a dict
uploaded_file_dict = uploaded_file_instance.to_dict()
# create an instance of UploadedFile from a dict
uploaded_file_from_dict = UploadedFile.from_dict(uploaded_file_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


