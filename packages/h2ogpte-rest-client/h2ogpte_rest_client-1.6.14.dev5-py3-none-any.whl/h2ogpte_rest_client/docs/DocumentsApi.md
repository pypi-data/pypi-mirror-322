# h2ogpte_rest_client.DocumentsApi

All URIs are relative to *https://h2ogpte.genai.h2o.ai/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_tag_on_document**](DocumentsApi.md#create_tag_on_document) | **POST** /documents/{document_id}/tags | Assigns a tag to the document.
[**delete_document**](DocumentsApi.md#delete_document) | **DELETE** /documents/{document_id} | Deletes a document.
[**delete_tag_from_document**](DocumentsApi.md#delete_tag_from_document) | **DELETE** /documents/{document_id}/tags/{tag_name} | Removes a tag from a document.
[**get_chat_session_count_for_document**](DocumentsApi.md#get_chat_session_count_for_document) | **GET** /documents/{document_id}/chats/count | Counts a number of chat sessions with the document.
[**get_document**](DocumentsApi.md#get_document) | **GET** /documents/{document_id} | Finds a document by id.
[**get_document_count**](DocumentsApi.md#get_document_count) | **GET** /documents/count | Counts a number of documents.
[**list_chat_sessions_for_document**](DocumentsApi.md#list_chat_sessions_for_document) | **GET** /documents/{document_id}/chats | List chat sessions for a given document.
[**list_collections_for_document**](DocumentsApi.md#list_collections_for_document) | **GET** /documents/{document_id}/collections | Lists collections for containing a given document.
[**list_documents**](DocumentsApi.md#list_documents) | **GET** /documents | List documents.
[**update_document**](DocumentsApi.md#update_document) | **PATCH** /documents/{document_id} | Updates attributes of an existing document.


# **create_tag_on_document**
> Tag create_tag_on_document(document_id, tag_create_request)

Assigns a tag to the document.

Assigns a tag to the document.

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
    api_instance = h2ogpte_rest_client.DocumentsApi(api_client)
    document_id = 'document_id_example' # str | Id of the document to to be associated with a tag
    tag_create_request = h2ogpte_rest_client.TagCreateRequest() # TagCreateRequest | 

    try:
        # Assigns a tag to the document.
        api_response = api_instance.create_tag_on_document(document_id, tag_create_request)
        print("The response of DocumentsApi->create_tag_on_document:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocumentsApi->create_tag_on_document: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **document_id** | **str**| Id of the document to to be associated with a tag | 
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

# **delete_document**
> delete_document(document_id, timeout=timeout)

Deletes a document.

Deletes a document with a given unique identifier.

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
    api_instance = h2ogpte_rest_client.DocumentsApi(api_client)
    document_id = 'document_id_example' # str | Id of document to delete
    timeout = 300 # int | Timeout in seconds (optional) (default to 300)

    try:
        # Deletes a document.
        api_instance.delete_document(document_id, timeout=timeout)
    except Exception as e:
        print("Exception when calling DocumentsApi->delete_document: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **document_id** | **str**| Id of document to delete | 
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

# **delete_tag_from_document**
> delete_tag_from_document(document_id, tag_name)

Removes a tag from a document.

Removes a tag from a document.

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
    api_instance = h2ogpte_rest_client.DocumentsApi(api_client)
    document_id = 'document_id_example' # str | Id of the document to remove the tag from
    tag_name = 'tag_name_example' # str | Name of the tag to be removed.

    try:
        # Removes a tag from a document.
        api_instance.delete_tag_from_document(document_id, tag_name)
    except Exception as e:
        print("Exception when calling DocumentsApi->delete_tag_from_document: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **document_id** | **str**| Id of the document to remove the tag from | 
 **tag_name** | **str**| Name of the tag to be removed. | 

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

# **get_chat_session_count_for_document**
> Count get_chat_session_count_for_document(document_id)

Counts a number of chat sessions with the document.

Counts a number of chat sessions with the document.

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
    api_instance = h2ogpte_rest_client.DocumentsApi(api_client)
    document_id = 'document_id_example' # str | Id of the document to filter by.

    try:
        # Counts a number of chat sessions with the document.
        api_response = api_instance.get_chat_session_count_for_document(document_id)
        print("The response of DocumentsApi->get_chat_session_count_for_document:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocumentsApi->get_chat_session_count_for_document: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **document_id** | **str**| Id of the document to filter by. | 

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

# **get_document**
> Document get_document(document_id)

Finds a document by id.

Returns a single document by its unique identifier.

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
    api_instance = h2ogpte_rest_client.DocumentsApi(api_client)
    document_id = 'document_id_example' # str | Id of document to return

    try:
        # Finds a document by id.
        api_response = api_instance.get_document(document_id)
        print("The response of DocumentsApi->get_document:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocumentsApi->get_document: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **document_id** | **str**| Id of document to return | 

### Return type

[**Document**](Document.md)

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

# **get_document_count**
> Count get_document_count()

Counts a number of documents.

Counts a number of documents.

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
    api_instance = h2ogpte_rest_client.DocumentsApi(api_client)

    try:
        # Counts a number of documents.
        api_response = api_instance.get_document_count()
        print("The response of DocumentsApi->get_document_count:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocumentsApi->get_document_count: %s\n" % e)
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

# **list_chat_sessions_for_document**
> List[ChatSession] list_chat_sessions_for_document(document_id, offset=offset, limit=limit)

List chat sessions for a given document.

List chat sessions for a given document.

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
    api_instance = h2ogpte_rest_client.DocumentsApi(api_client)
    document_id = 'document_id_example' # str | Id of the document to filter by.
    offset = 0 # int | How many chat sessions to skip before returning. (optional) (default to 0)
    limit = 100 # int | How many chat sessions to return. (optional) (default to 100)

    try:
        # List chat sessions for a given document.
        api_response = api_instance.list_chat_sessions_for_document(document_id, offset=offset, limit=limit)
        print("The response of DocumentsApi->list_chat_sessions_for_document:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocumentsApi->list_chat_sessions_for_document: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **document_id** | **str**| Id of the document to filter by. | 
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

# **list_collections_for_document**
> List[Collection] list_collections_for_document(document_id, offset=offset, limit=limit)

Lists collections for containing a given document.

Lists collections for containing a given document.

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
    api_instance = h2ogpte_rest_client.DocumentsApi(api_client)
    document_id = 'document_id_example' # str | Id of the document.
    offset = 0 # int | How many collections to skip before returning. (optional) (default to 0)
    limit = 100 # int | How many collections to return. (optional) (default to 100)

    try:
        # Lists collections for containing a given document.
        api_response = api_instance.list_collections_for_document(document_id, offset=offset, limit=limit)
        print("The response of DocumentsApi->list_collections_for_document:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocumentsApi->list_collections_for_document: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **document_id** | **str**| Id of the document. | 
 **offset** | **int**| How many collections to skip before returning. | [optional] [default to 0]
 **limit** | **int**| How many collections to return. | [optional] [default to 100]

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

# **list_documents**
> List[Document] list_documents(offset=offset, limit=limit, sort_column=sort_column, ascending=ascending, with_summaries=with_summaries)

List documents.

List documents for a given user. If sort_column is not specified, the output is sorted by by last update time in descending order.

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
    api_instance = h2ogpte_rest_client.DocumentsApi(api_client)
    offset = 0 # int | How many collections to skip before returning. (optional) (default to 0)
    limit = 100 # int | How many documents to return. (optional) (default to 100)
    sort_column = updated_at # str | Sort column. (optional) (default to updated_at)
    ascending = False # bool | When true, returns sorted by sort_column in ascending order. (optional) (default to False)
    with_summaries = False # bool | When true, returns also summary and summary_parameter with other common attributes of the document. (optional) (default to False)

    try:
        # List documents.
        api_response = api_instance.list_documents(offset=offset, limit=limit, sort_column=sort_column, ascending=ascending, with_summaries=with_summaries)
        print("The response of DocumentsApi->list_documents:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocumentsApi->list_documents: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **int**| How many collections to skip before returning. | [optional] [default to 0]
 **limit** | **int**| How many documents to return. | [optional] [default to 100]
 **sort_column** | **str**| Sort column. | [optional] [default to updated_at]
 **ascending** | **bool**| When true, returns sorted by sort_column in ascending order. | [optional] [default to False]
 **with_summaries** | **bool**| When true, returns also summary and summary_parameter with other common attributes of the document. | [optional] [default to False]

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

# **update_document**
> Document update_document(document_id, document_update_request)

Updates attributes of an existing document.

Updates attributes of an existing document, particularly name and uri.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.document import Document
from h2ogpte_rest_client.models.document_update_request import DocumentUpdateRequest
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
    api_instance = h2ogpte_rest_client.DocumentsApi(api_client)
    document_id = 'document_id_example' # str | Id of document to to be updated
    document_update_request = h2ogpte_rest_client.DocumentUpdateRequest() # DocumentUpdateRequest | 

    try:
        # Updates attributes of an existing document.
        api_response = api_instance.update_document(document_id, document_update_request)
        print("The response of DocumentsApi->update_document:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocumentsApi->update_document: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **document_id** | **str**| Id of document to to be updated | 
 **document_update_request** | [**DocumentUpdateRequest**](DocumentUpdateRequest.md)|  | 

### Return type

[**Document**](Document.md)

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

