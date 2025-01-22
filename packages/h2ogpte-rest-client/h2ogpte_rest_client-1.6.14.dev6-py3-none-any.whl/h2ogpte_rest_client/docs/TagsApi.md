# h2ogpte_rest_client.TagsApi

All URIs are relative to *https://h2ogpte.genai.h2o.ai/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_tag**](TagsApi.md#create_tag) | **POST** /tags | Creates a new tag.
[**get_tag**](TagsApi.md#get_tag) | **GET** /tags/{tag_name} | Finds a tag by its name.
[**list_documents_for_tag**](TagsApi.md#list_documents_for_tag) | **GET** /tags/{tag_name}/documents | List documents associated with a tag.
[**list_tags**](TagsApi.md#list_tags) | **GET** /tags | List tags.
[**update_tag**](TagsApi.md#update_tag) | **PATCH** /tags/{tag_name} | Updates attributes of a tag.


# **create_tag**
> Tag create_tag(tag_create_request)

Creates a new tag.

Creates a new tag that can be subsequently associated with a document.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.tag import Tag
from h2ogpte_rest_client.models.tag_create_request import TagCreateRequest
from h2ogpte_rest_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://h2ogpte.genai.h2o.ai/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = h2ogpte_rest_client.Configuration(
    host = "https://h2ogpte.genai.h2o.ai/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: bearerAuth
configuration = h2ogpte_rest_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with h2ogpte_rest_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = h2ogpte_rest_client.TagsApi(api_client)
    tag_create_request = h2ogpte_rest_client.TagCreateRequest() # TagCreateRequest | 

    try:
        # Creates a new tag.
        api_response = api_instance.create_tag(tag_create_request)
        print("The response of TagsApi->create_tag:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TagsApi->create_tag: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tag_create_request** | [**TagCreateRequest**](TagCreateRequest.md)|  | 

### Return type

[**Tag**](Tag.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful operation |  -  |
**401** | Unauthorized - Invalid or missing API key |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_tag**
> Tag get_tag(tag_name)

Finds a tag by its name.

Returns a single tag by its unique name.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.tag import Tag
from h2ogpte_rest_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://h2ogpte.genai.h2o.ai/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = h2ogpte_rest_client.Configuration(
    host = "https://h2ogpte.genai.h2o.ai/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: bearerAuth
configuration = h2ogpte_rest_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with h2ogpte_rest_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = h2ogpte_rest_client.TagsApi(api_client)
    tag_name = 'tag_name_example' # str | Name of a tag to return

    try:
        # Finds a tag by its name.
        api_response = api_instance.get_tag(tag_name)
        print("The response of TagsApi->get_tag:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TagsApi->get_tag: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tag_name** | **str**| Name of a tag to return | 

### Return type

[**Tag**](Tag.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful operation |  -  |
**401** | Unauthorized - Invalid or missing API key |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_documents_for_tag**
> List[Document] list_documents_for_tag(tag_name, collection_id)

List documents associated with a tag.

List documents associated with a tag.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.document import Document
from h2ogpte_rest_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://h2ogpte.genai.h2o.ai/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = h2ogpte_rest_client.Configuration(
    host = "https://h2ogpte.genai.h2o.ai/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: bearerAuth
configuration = h2ogpte_rest_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with h2ogpte_rest_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = h2ogpte_rest_client.TagsApi(api_client)
    tag_name = 'tag_name_example' # str | Name of a tag to return documents for
    collection_id = 'collection_id_example' # str | Id of a collection containing the documents

    try:
        # List documents associated with a tag.
        api_response = api_instance.list_documents_for_tag(tag_name, collection_id)
        print("The response of TagsApi->list_documents_for_tag:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TagsApi->list_documents_for_tag: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tag_name** | **str**| Name of a tag to return documents for | 
 **collection_id** | **str**| Id of a collection containing the documents | 

### Return type

[**List[Document]**](Document.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful operation |  -  |
**401** | Unauthorized - Invalid or missing API key |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_tags**
> List[Tag] list_tags()

List tags.

List all existing tags.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.tag import Tag
from h2ogpte_rest_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://h2ogpte.genai.h2o.ai/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = h2ogpte_rest_client.Configuration(
    host = "https://h2ogpte.genai.h2o.ai/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: bearerAuth
configuration = h2ogpte_rest_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with h2ogpte_rest_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = h2ogpte_rest_client.TagsApi(api_client)

    try:
        # List tags.
        api_response = api_instance.list_tags()
        print("The response of TagsApi->list_tags:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TagsApi->list_tags: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[Tag]**](Tag.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful operation |  -  |
**401** | Unauthorized - Invalid or missing API key |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_tag**
> Collection update_tag(tag_name, tag_update_request)

Updates attributes of a tag.

Updates attributes of an existing tag, particularly description and format.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.collection import Collection
from h2ogpte_rest_client.models.tag_update_request import TagUpdateRequest
from h2ogpte_rest_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://h2ogpte.genai.h2o.ai/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = h2ogpte_rest_client.Configuration(
    host = "https://h2ogpte.genai.h2o.ai/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: bearerAuth
configuration = h2ogpte_rest_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with h2ogpte_rest_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = h2ogpte_rest_client.TagsApi(api_client)
    tag_name = 'tag_name_example' # str | Name of a tag to to be updated
    tag_update_request = h2ogpte_rest_client.TagUpdateRequest() # TagUpdateRequest | 

    try:
        # Updates attributes of a tag.
        api_response = api_instance.update_tag(tag_name, tag_update_request)
        print("The response of TagsApi->update_tag:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TagsApi->update_tag: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tag_name** | **str**| Name of a tag to to be updated | 
 **tag_update_request** | [**TagUpdateRequest**](TagUpdateRequest.md)|  | 

### Return type

[**Collection**](Collection.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful operation |  -  |
**401** | Unauthorized - Invalid or missing API key |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

