# IngestFromWebsiteRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** | String of the url to crawl. | 

## Example

```python
from h2ogpte_rest_client.models.ingest_from_website_request import IngestFromWebsiteRequest

# TODO update the JSON string below
json = "{}"
# create an instance of IngestFromWebsiteRequest from a JSON string
ingest_from_website_request_instance = IngestFromWebsiteRequest.from_json(json)
# print the JSON string representation of the object
print(IngestFromWebsiteRequest.to_json())

# convert the object into a dict
ingest_from_website_request_dict = ingest_from_website_request_instance.to_dict()
# create an instance of IngestFromWebsiteRequest from a dict
ingest_from_website_request_from_dict = IngestFromWebsiteRequest.from_dict(ingest_from_website_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


