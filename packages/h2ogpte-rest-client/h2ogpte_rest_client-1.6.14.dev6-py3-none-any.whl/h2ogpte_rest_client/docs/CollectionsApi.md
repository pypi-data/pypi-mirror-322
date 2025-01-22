# h2ogpte_rest_client.CollectionsApi

All URIs are relative to *https://h2ogpte.genai.h2o.ai/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_collection**](CollectionsApi.md#create_collection) | **POST** /collections | Create a Collection
[**delete_collection**](CollectionsApi.md#delete_collection) | **DELETE** /collections/{collection_id} | Deletes collection.
[**delete_collection_prompt_template**](CollectionsApi.md#delete_collection_prompt_template) | **DELETE** /collections/{collection_id}/prompt_template | Removes a prompt template reference from the collection.
[**delete_collection_thumbnail**](CollectionsApi.md#delete_collection_thumbnail) | **DELETE** /collections/{collection_id}/thumbnail | Deletes collection thumbnail.
[**delete_document_from_collection**](CollectionsApi.md#delete_document_from_collection) | **DELETE** /collections/{collection_id}/documents/{document_id} | Removes the document from the collection.
[**get_chat_session_count_for_collection**](CollectionsApi.md#get_chat_session_count_for_collection) | **GET** /collections/{collection_id}/chats/count | Counts a number of chat sessions with the collection.
[**get_collection**](CollectionsApi.md#get_collection) | **GET** /collections/{collection_id} | Get a Collection
[**get_collection_chat_settings**](CollectionsApi.md#get_collection_chat_settings) | **GET** /collections/{collection_id}/chat_settings | Fetches collection chat settings.
[**get_collection_count**](CollectionsApi.md#get_collection_count) | **GET** /collections/count | Counts a number of collections.
[**get_collection_permissions**](CollectionsApi.md#get_collection_permissions) | **GET** /collections/{collection_id}/permissions | Returns a list of access permissions for a given collection.
[**get_collection_settings**](CollectionsApi.md#get_collection_settings) | **GET** /collections/{collection_id}/settings | Fetches collection settings.
[**get_document_count_for_collection**](CollectionsApi.md#get_document_count_for_collection) | **GET** /collections/{collection_id}/documents/count | Counts a number of documents in the collection.
[**insert_document_into_collection**](CollectionsApi.md#insert_document_into_collection) | **PUT** /collections/{collection_id}/documents/{document_id} | Import an already stored document to an existing collection.
[**list_chat_sessions_for_collection**](CollectionsApi.md#list_chat_sessions_for_collection) | **GET** /collections/{collection_id}/chats | List chat sessions for a given collection.
[**list_collections**](CollectionsApi.md#list_collections) | **GET** /collections | List collections.
[**list_documents_for_collection**](CollectionsApi.md#list_documents_for_collection) | **GET** /collections/{collection_id}/documents | List a Collection&#39;s documents
[**list_questions_for_collection**](CollectionsApi.md#list_questions_for_collection) | **GET** /collections/{collection_id}/questions | List suggested questions for a given collection.
[**share_collection**](CollectionsApi.md#share_collection) | **PUT** /collections/{collection_id}/permissions/{username} | Shares a collection to a user.
[**unshare_collection**](CollectionsApi.md#unshare_collection) | **DELETE** /collections/{collection_id}/permissions/{username} | Removes sharing of a collection to a user.
[**unshare_collection_for_all**](CollectionsApi.md#unshare_collection_for_all) | **DELETE** /collections/{collection_id}/permissions | Removes sharing of a collection to all other users except the original owner.
[**update_collection**](CollectionsApi.md#update_collection) | **PATCH** /collections/{collection_id} | Updates attributes of an existing collection.
[**update_collection_chat_settings**](CollectionsApi.md#update_collection_chat_settings) | **PUT** /collections/{collection_id}/chat_settings | Updates collection chat settings.
[**update_collection_prompt_template**](CollectionsApi.md#update_collection_prompt_template) | **PUT** /collections/{collection_id}/prompt_template | Updates a prompt template reference of a collection.
[**update_collection_settings**](CollectionsApi.md#update_collection_settings) | **PUT** /collections/{collection_id}/settings | Updates collection settings.
[**update_collection_thumbnail**](CollectionsApi.md#update_collection_thumbnail) | **PUT** /collections/{collection_id}/thumbnail | Updates collection thumbnail.


# **create_collection**
> Collection create_collection(collection_create_request)

Create a Collection

A Collection refers to a group of related Documents. A Collection lets a user aggregate documents in one location. A user can utilize Collections to group particular sets of material (documents) to explore individually through Chats utilizing a large language model (LLM).

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.collection import Collection
from h2ogpte_rest_client.models.collection_create_request import CollectionCreateRequest
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
    api_instance = h2ogpte_rest_client.CollectionsApi(api_client)
    collection_create_request = h2ogpte_rest_client.CollectionCreateRequest() # CollectionCreateRequest | 

    try:
        # Create a Collection
        api_response = api_instance.create_collection(collection_create_request)
        print("The response of CollectionsApi->create_collection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->create_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_create_request** | [**CollectionCreateRequest**](CollectionCreateRequest.md)|  | 

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
**201** | Successful operation |  -  |
**401** | Unauthorized - Invalid or missing API key |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_collection**
> delete_collection(collection_id, timeout=timeout)

Deletes collection.

Deletes collection with a given unique identifier.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
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
    api_instance = h2ogpte_rest_client.CollectionsApi(api_client)
    collection_id = 'collection_id_example' # str | Id of collection to delete
    timeout = 300 # int | Timeout in seconds (optional) (default to 300)

    try:
        # Deletes collection.
        api_instance.delete_collection(collection_id, timeout=timeout)
    except Exception as e:
        print("Exception when calling CollectionsApi->delete_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Id of collection to delete | 
 **timeout** | **int**| Timeout in seconds | [optional] [default to 300]

### Return type

void (empty response body)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful operation |  -  |
**401** | Unauthorized - Invalid or missing API key |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_collection_prompt_template**
> Collection delete_collection_prompt_template(collection_id)

Removes a prompt template reference from the collection.

Removes a prompt template reference from the collection.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.collection import Collection
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
    api_instance = h2ogpte_rest_client.CollectionsApi(api_client)
    collection_id = 'collection_id_example' # str | Id of the collection

    try:
        # Removes a prompt template reference from the collection.
        api_response = api_instance.delete_collection_prompt_template(collection_id)
        print("The response of CollectionsApi->delete_collection_prompt_template:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->delete_collection_prompt_template: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Id of the collection | 

### Return type

[**Collection**](Collection.md)

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

# **delete_collection_thumbnail**
> delete_collection_thumbnail(collection_id, timeout=timeout)

Deletes collection thumbnail.

Deletes collection thumbnail image.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
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
    api_instance = h2ogpte_rest_client.CollectionsApi(api_client)
    collection_id = 'collection_id_example' # str | Id of the collection
    timeout = 300 # int | Timeout in seconds (optional) (default to 300)

    try:
        # Deletes collection thumbnail.
        api_instance.delete_collection_thumbnail(collection_id, timeout=timeout)
    except Exception as e:
        print("Exception when calling CollectionsApi->delete_collection_thumbnail: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Id of the collection | 
 **timeout** | **int**| Timeout in seconds | [optional] [default to 300]

### Return type

void (empty response body)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful operation |  -  |
**401** | Unauthorized - Invalid or missing API key |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_document_from_collection**
> delete_document_from_collection(collection_id, document_id, timeout=timeout)

Removes the document from the collection.

Removes the document from the collection.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
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
    api_instance = h2ogpte_rest_client.CollectionsApi(api_client)
    collection_id = 'collection_id_example' # str | Id of the collection to remove the document from.
    document_id = 'document_id_example' # str | Id of the document to be removed.
    timeout = 300 # int | Timeout in seconds (optional) (default to 300)

    try:
        # Removes the document from the collection.
        api_instance.delete_document_from_collection(collection_id, document_id, timeout=timeout)
    except Exception as e:
        print("Exception when calling CollectionsApi->delete_document_from_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Id of the collection to remove the document from. | 
 **document_id** | **str**| Id of the document to be removed. | 
 **timeout** | **int**| Timeout in seconds | [optional] [default to 300]

### Return type

void (empty response body)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful operation |  -  |
**401** | Unauthorized - Invalid or missing API key |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_chat_session_count_for_collection**
> Count get_chat_session_count_for_collection(collection_id)

Counts a number of chat sessions with the collection.

Counts a number of chat sessions with the collection.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.count import Count
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
    api_instance = h2ogpte_rest_client.CollectionsApi(api_client)
    collection_id = 'collection_id_example' # str | Id of the collection to filter by.

    try:
        # Counts a number of chat sessions with the collection.
        api_response = api_instance.get_chat_session_count_for_collection(collection_id)
        print("The response of CollectionsApi->get_chat_session_count_for_collection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->get_chat_session_count_for_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Id of the collection to filter by. | 

### Return type

[**Count**](Count.md)

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

# **get_collection**
> Collection get_collection(collection_id)

Get a Collection

A user can obtain a Collection by specifying its ID.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.collection import Collection
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
    api_instance = h2ogpte_rest_client.CollectionsApi(api_client)
    collection_id = 'collection_id_example' # str | Id of collection to return

    try:
        # Get a Collection
        api_response = api_instance.get_collection(collection_id)
        print("The response of CollectionsApi->get_collection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->get_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Id of collection to return | 

### Return type

[**Collection**](Collection.md)

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

# **get_collection_chat_settings**
> ChatSettings get_collection_chat_settings(collection_id)

Fetches collection chat settings.

Returns details of collection chat settings

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.chat_settings import ChatSettings
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
    api_instance = h2ogpte_rest_client.CollectionsApi(api_client)
    collection_id = 'collection_id_example' # str | Id of the collection associated with the chat settings

    try:
        # Fetches collection chat settings.
        api_response = api_instance.get_collection_chat_settings(collection_id)
        print("The response of CollectionsApi->get_collection_chat_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->get_collection_chat_settings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Id of the collection associated with the chat settings | 

### Return type

[**ChatSettings**](ChatSettings.md)

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

# **get_collection_count**
> Count get_collection_count()

Counts a number of collections.

Counts a number of collections.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.count import Count
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
    api_instance = h2ogpte_rest_client.CollectionsApi(api_client)

    try:
        # Counts a number of collections.
        api_response = api_instance.get_collection_count()
        print("The response of CollectionsApi->get_collection_count:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->get_collection_count: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**Count**](Count.md)

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

# **get_collection_permissions**
> List[SharePermission] get_collection_permissions(collection_id)

Returns a list of access permissions for a given collection.

The returned list of permissions denotes who has access to the collection.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.share_permission import SharePermission
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
    api_instance = h2ogpte_rest_client.CollectionsApi(api_client)
    collection_id = 'collection_id_example' # str | Id of the collection.

    try:
        # Returns a list of access permissions for a given collection.
        api_response = api_instance.get_collection_permissions(collection_id)
        print("The response of CollectionsApi->get_collection_permissions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->get_collection_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Id of the collection. | 

### Return type

[**List[SharePermission]**](SharePermission.md)

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

# **get_collection_settings**
> CollectionSettings get_collection_settings(collection_id)

Fetches collection settings.

Returns details of collection settings

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.collection_settings import CollectionSettings
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
    api_instance = h2ogpte_rest_client.CollectionsApi(api_client)
    collection_id = 'collection_id_example' # str | Id of the collection associated with the settings

    try:
        # Fetches collection settings.
        api_response = api_instance.get_collection_settings(collection_id)
        print("The response of CollectionsApi->get_collection_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->get_collection_settings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Id of the collection associated with the settings | 

### Return type

[**CollectionSettings**](CollectionSettings.md)

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

# **get_document_count_for_collection**
> Count get_document_count_for_collection(collection_id)

Counts a number of documents in the collection.

Counts a number of documents in the collection.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.count import Count
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
    api_instance = h2ogpte_rest_client.CollectionsApi(api_client)
    collection_id = 'collection_id_example' # str | Id of the collection to filter by.

    try:
        # Counts a number of documents in the collection.
        api_response = api_instance.get_document_count_for_collection(collection_id)
        print("The response of CollectionsApi->get_document_count_for_collection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->get_document_count_for_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Id of the collection to filter by. | 

### Return type

[**Count**](Count.md)

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

# **insert_document_into_collection**
> insert_document_into_collection(collection_id, document_id, timeout=timeout, gen_doc_summaries=gen_doc_summaries, gen_doc_questions=gen_doc_questions, copy_document=copy_document, ocr_model=ocr_model, tesseract_lang=tesseract_lang, keep_tables_as_one_chunk=keep_tables_as_one_chunk, chunk_by_page=chunk_by_page, handwriting_check=handwriting_check)

Import an already stored document to an existing collection.

Import an already stored document to an existing collection.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
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
    api_instance = h2ogpte_rest_client.CollectionsApi(api_client)
    collection_id = 'collection_id_example' # str | Id of the collection to remove the document from.
    document_id = 'document_id_example' # str | Id of the document to be removed.
    timeout = 300 # int | Timeout in seconds (optional) (default to 300)
    gen_doc_summaries = False # bool | Whether to auto-generate document summaries (uses LLM) (optional) (default to False)
    gen_doc_questions = False # bool | Whether to auto-generate sample questions for each document (uses LLM) (optional) (default to False)
    copy_document = False # bool | Whether to save a new copy of the document. (optional) (default to False)
    ocr_model = 'auto' # str | Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models (optional) (default to 'auto')
    tesseract_lang = 'tesseract_lang_example' # str | Which language to use when using `ocr_model=\"tesseract\"`. (optional)
    keep_tables_as_one_chunk = False # bool | When tables are identified by the table parser the table tokens will be kept in a single chunk. (optional) (default to False)
    chunk_by_page = False # bool | Each page will be a chunk. `keep_tables_as_one_chunk` will be ignored if this is `true`. (optional) (default to False)
    handwriting_check = False # bool | Check pages for handwriting. Will use specialized models if handwriting is found. (optional) (default to False)

    try:
        # Import an already stored document to an existing collection.
        api_instance.insert_document_into_collection(collection_id, document_id, timeout=timeout, gen_doc_summaries=gen_doc_summaries, gen_doc_questions=gen_doc_questions, copy_document=copy_document, ocr_model=ocr_model, tesseract_lang=tesseract_lang, keep_tables_as_one_chunk=keep_tables_as_one_chunk, chunk_by_page=chunk_by_page, handwriting_check=handwriting_check)
    except Exception as e:
        print("Exception when calling CollectionsApi->insert_document_into_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Id of the collection to remove the document from. | 
 **document_id** | **str**| Id of the document to be removed. | 
 **timeout** | **int**| Timeout in seconds | [optional] [default to 300]
 **gen_doc_summaries** | **bool**| Whether to auto-generate document summaries (uses LLM) | [optional] [default to False]
 **gen_doc_questions** | **bool**| Whether to auto-generate sample questions for each document (uses LLM) | [optional] [default to False]
 **copy_document** | **bool**| Whether to save a new copy of the document. | [optional] [default to False]
 **ocr_model** | **str**| Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models | [optional] [default to &#39;auto&#39;]
 **tesseract_lang** | **str**| Which language to use when using &#x60;ocr_model&#x3D;\&quot;tesseract\&quot;&#x60;. | [optional] 
 **keep_tables_as_one_chunk** | **bool**| When tables are identified by the table parser the table tokens will be kept in a single chunk. | [optional] [default to False]
 **chunk_by_page** | **bool**| Each page will be a chunk. &#x60;keep_tables_as_one_chunk&#x60; will be ignored if this is &#x60;true&#x60;. | [optional] [default to False]
 **handwriting_check** | **bool**| Check pages for handwriting. Will use specialized models if handwriting is found. | [optional] [default to False]

### Return type

void (empty response body)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful operation |  -  |
**401** | Unauthorized - Invalid or missing API key |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_chat_sessions_for_collection**
> List[ChatSession] list_chat_sessions_for_collection(collection_id, offset=offset, limit=limit)

List chat sessions for a given collection.

List chat sessions for a given collection.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.chat_session import ChatSession
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
    api_instance = h2ogpte_rest_client.CollectionsApi(api_client)
    collection_id = 'collection_id_example' # str | Id of the collection to filter by.
    offset = 0 # int | How many chat sessions to skip before returning. (optional) (default to 0)
    limit = 100 # int | How many chat sessions to return. (optional) (default to 100)

    try:
        # List chat sessions for a given collection.
        api_response = api_instance.list_chat_sessions_for_collection(collection_id, offset=offset, limit=limit)
        print("The response of CollectionsApi->list_chat_sessions_for_collection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->list_chat_sessions_for_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Id of the collection to filter by. | 
 **offset** | **int**| How many chat sessions to skip before returning. | [optional] [default to 0]
 **limit** | **int**| How many chat sessions to return. | [optional] [default to 100]

### Return type

[**List[ChatSession]**](ChatSession.md)

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

# **list_collections**
> List[Collection] list_collections(offset=offset, limit=limit, sort_column=sort_column, ascending=ascending)

List collections.

List collections for a given user. If sort_column is not specified, the output is sorted by by last update time in descending order.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.collection import Collection
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
    api_instance = h2ogpte_rest_client.CollectionsApi(api_client)
    offset = 0 # int | How many collections to skip before returning. (optional) (default to 0)
    limit = 100 # int | How many collections to return. (optional) (default to 100)
    sort_column = updated_at # str | Sort column. (optional) (default to updated_at)
    ascending = False # bool | When true, returns sorted by sort_column in ascending order. (optional) (default to False)

    try:
        # List collections.
        api_response = api_instance.list_collections(offset=offset, limit=limit, sort_column=sort_column, ascending=ascending)
        print("The response of CollectionsApi->list_collections:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->list_collections: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **int**| How many collections to skip before returning. | [optional] [default to 0]
 **limit** | **int**| How many collections to return. | [optional] [default to 100]
 **sort_column** | **str**| Sort column. | [optional] [default to updated_at]
 **ascending** | **bool**| When true, returns sorted by sort_column in ascending order. | [optional] [default to False]

### Return type

[**List[Collection]**](Collection.md)

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

# **list_documents_for_collection**
> List[Document] list_documents_for_collection(collection_id, offset=offset, limit=limit)

List a Collection's documents

A user can list a Collection's documents.

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
    api_instance = h2ogpte_rest_client.CollectionsApi(api_client)
    collection_id = 'collection_id_example' # str | This parameter refers to the unique identifier ( ID) of the Collection to filter results.
    offset = 0 # int | This parameter refers to the number of documents to skip before retrieving results. (optional) (default to 0)
    limit = 100 # int | This parameter refers to the maximum number of documents to return in the result set. (optional) (default to 100)

    try:
        # List a Collection's documents
        api_response = api_instance.list_documents_for_collection(collection_id, offset=offset, limit=limit)
        print("The response of CollectionsApi->list_documents_for_collection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->list_documents_for_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| This parameter refers to the unique identifier ( ID) of the Collection to filter results. | 
 **offset** | **int**| This parameter refers to the number of documents to skip before retrieving results. | [optional] [default to 0]
 **limit** | **int**| This parameter refers to the maximum number of documents to return in the result set. | [optional] [default to 100]

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

# **list_questions_for_collection**
> List[SuggestedQuestion] list_questions_for_collection(collection_id, limit=limit)

List suggested questions for a given collection.

List suggested questions for a given collection.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.suggested_question import SuggestedQuestion
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
    api_instance = h2ogpte_rest_client.CollectionsApi(api_client)
    collection_id = 'collection_id_example' # str | Id of the collection to filter by.
    limit = 100 # int | How many questions to return. (optional) (default to 100)

    try:
        # List suggested questions for a given collection.
        api_response = api_instance.list_questions_for_collection(collection_id, limit=limit)
        print("The response of CollectionsApi->list_questions_for_collection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->list_questions_for_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Id of the collection to filter by. | 
 **limit** | **int**| How many questions to return. | [optional] [default to 100]

### Return type

[**List[SuggestedQuestion]**](SuggestedQuestion.md)

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

# **share_collection**
> share_collection(collection_id, username)

Shares a collection to a user.

Shares a collection template to a user.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
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
    api_instance = h2ogpte_rest_client.CollectionsApi(api_client)
    collection_id = 'collection_id_example' # str | Id of the collection.
    username = 'username_example' # str | User name that will obtain access to the collection

    try:
        # Shares a collection to a user.
        api_instance.share_collection(collection_id, username)
    except Exception as e:
        print("Exception when calling CollectionsApi->share_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Id of the collection. | 
 **username** | **str**| User name that will obtain access to the collection | 

### Return type

void (empty response body)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful operation |  -  |
**401** | Unauthorized - Invalid or missing API key |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unshare_collection**
> unshare_collection(collection_id, username)

Removes sharing of a collection to a user.

Removes sharing of a collection to a user.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
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
    api_instance = h2ogpte_rest_client.CollectionsApi(api_client)
    collection_id = 'collection_id_example' # str | Id of the collection.
    username = 'username_example' # str | User name that will lose access to the collection

    try:
        # Removes sharing of a collection to a user.
        api_instance.unshare_collection(collection_id, username)
    except Exception as e:
        print("Exception when calling CollectionsApi->unshare_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Id of the collection. | 
 **username** | **str**| User name that will lose access to the collection | 

### Return type

void (empty response body)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful operation |  -  |
**401** | Unauthorized - Invalid or missing API key |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unshare_collection_for_all**
> unshare_collection_for_all(collection_id)

Removes sharing of a collection to all other users except the original owner.

Removes sharing of a collection to all other users except the original owner.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
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
    api_instance = h2ogpte_rest_client.CollectionsApi(api_client)
    collection_id = 'collection_id_example' # str | Id of the collection.

    try:
        # Removes sharing of a collection to all other users except the original owner.
        api_instance.unshare_collection_for_all(collection_id)
    except Exception as e:
        print("Exception when calling CollectionsApi->unshare_collection_for_all: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Id of the collection. | 

### Return type

void (empty response body)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful operation |  -  |
**401** | Unauthorized - Invalid or missing API key |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_collection**
> Collection update_collection(collection_id, collection_update_request)

Updates attributes of an existing collection.

Updates of an existing collection, particularly name and description.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.collection import Collection
from h2ogpte_rest_client.models.collection_update_request import CollectionUpdateRequest
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
    api_instance = h2ogpte_rest_client.CollectionsApi(api_client)
    collection_id = 'collection_id_example' # str | Id of collection to to be updated
    collection_update_request = h2ogpte_rest_client.CollectionUpdateRequest() # CollectionUpdateRequest | 

    try:
        # Updates attributes of an existing collection.
        api_response = api_instance.update_collection(collection_id, collection_update_request)
        print("The response of CollectionsApi->update_collection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->update_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Id of collection to to be updated | 
 **collection_update_request** | [**CollectionUpdateRequest**](CollectionUpdateRequest.md)|  | 

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

# **update_collection_chat_settings**
> update_collection_chat_settings(collection_id, chat_settings=chat_settings)

Updates collection chat settings.

Recreates entire chat settings on the collection.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.chat_settings import ChatSettings
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
    api_instance = h2ogpte_rest_client.CollectionsApi(api_client)
    collection_id = 'collection_id_example' # str | Id of the collection
    chat_settings = h2ogpte_rest_client.ChatSettings() # ChatSettings |  (optional)

    try:
        # Updates collection chat settings.
        api_instance.update_collection_chat_settings(collection_id, chat_settings=chat_settings)
    except Exception as e:
        print("Exception when calling CollectionsApi->update_collection_chat_settings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Id of the collection | 
 **chat_settings** | [**ChatSettings**](ChatSettings.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful operation |  -  |
**401** | Unauthorized - Invalid or missing API key |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_collection_prompt_template**
> Collection update_collection_prompt_template(collection_id, prompt_template_change_request)

Updates a prompt template reference of a collection.

Updates a prompt template reference of a collection.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.collection import Collection
from h2ogpte_rest_client.models.prompt_template_change_request import PromptTemplateChangeRequest
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
    api_instance = h2ogpte_rest_client.CollectionsApi(api_client)
    collection_id = 'collection_id_example' # str | Id of the collection
    prompt_template_change_request = h2ogpte_rest_client.PromptTemplateChangeRequest() # PromptTemplateChangeRequest | 

    try:
        # Updates a prompt template reference of a collection.
        api_response = api_instance.update_collection_prompt_template(collection_id, prompt_template_change_request)
        print("The response of CollectionsApi->update_collection_prompt_template:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->update_collection_prompt_template: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Id of the collection | 
 **prompt_template_change_request** | [**PromptTemplateChangeRequest**](PromptTemplateChangeRequest.md)|  | 

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

# **update_collection_settings**
> update_collection_settings(collection_id, collection_settings=collection_settings)

Updates collection settings.

Recreates entire settings on the collection.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.collection_settings import CollectionSettings
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
    api_instance = h2ogpte_rest_client.CollectionsApi(api_client)
    collection_id = 'collection_id_example' # str | Id of the collection
    collection_settings = h2ogpte_rest_client.CollectionSettings() # CollectionSettings |  (optional)

    try:
        # Updates collection settings.
        api_instance.update_collection_settings(collection_id, collection_settings=collection_settings)
    except Exception as e:
        print("Exception when calling CollectionsApi->update_collection_settings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Id of the collection | 
 **collection_settings** | [**CollectionSettings**](CollectionSettings.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful operation |  -  |
**401** | Unauthorized - Invalid or missing API key |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_collection_thumbnail**
> update_collection_thumbnail(collection_id, timeout=timeout, file=file)

Updates collection thumbnail.

Uploads a new thumbnail image for the collection.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
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
    api_instance = h2ogpte_rest_client.CollectionsApi(api_client)
    collection_id = 'collection_id_example' # str | Id of the collection
    timeout = 300 # int | Timeout in seconds (optional) (default to 300)
    file = None # bytearray |  (optional)

    try:
        # Updates collection thumbnail.
        api_instance.update_collection_thumbnail(collection_id, timeout=timeout, file=file)
    except Exception as e:
        print("Exception when calling CollectionsApi->update_collection_thumbnail: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Id of the collection | 
 **timeout** | **int**| Timeout in seconds | [optional] [default to 300]
 **file** | **bytearray**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful operation |  -  |
**401** | Unauthorized - Invalid or missing API key |  -  |
**413** | Request entity is too large |  -  |
**415** | Unsupported media type |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

