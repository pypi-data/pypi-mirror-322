# h2ogpte_rest_client.ChatApi

All URIs are relative to *https://h2ogpte.genai.h2o.ai/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_chat_session**](ChatApi.md#create_chat_session) | **POST** /chats | Creates chat session.
[**delete_chat_session**](ChatApi.md#delete_chat_session) | **DELETE** /chats/{session_id} | Deletes collection.
[**delete_chat_session_collection**](ChatApi.md#delete_chat_session_collection) | **DELETE** /chats/{session_id}/collection | Removes a collection reference from the chat session.
[**delete_chat_session_prompt_template**](ChatApi.md#delete_chat_session_prompt_template) | **DELETE** /chats/{session_id}/prompt_template | Removes a prompt template reference from the chat session.
[**get_chat_session**](ChatApi.md#get_chat_session) | **GET** /chats/{session_id} | Finds a chat session by id.
[**get_chat_session_count**](ChatApi.md#get_chat_session_count) | **GET** /chats/count | Counts a number of chat sessions.
[**get_chat_session_messages**](ChatApi.md#get_chat_session_messages) | **GET** /chats/{session_id}/messages | Fetches chat message and metadata for messages in a chat session.
[**get_completion**](ChatApi.md#get_completion) | **POST** /chats/{session_id}/completions | 
[**get_message_meta**](ChatApi.md#get_message_meta) | **GET** /messages/{message_id}/meta | Fetches chat message meta information.
[**get_message_references**](ChatApi.md#get_message_references) | **GET** /messages/{message_id}/references | Fetches metadata for references of a chat message.
[**list_chat_sessions**](ChatApi.md#list_chat_sessions) | **GET** /chats | List chat sessions.
[**list_questions_for_chat_session**](ChatApi.md#list_questions_for_chat_session) | **GET** /chats/{session_id}/questions | List suggested questions for a given chat session.
[**update_chat_session**](ChatApi.md#update_chat_session) | **PATCH** /chats/{session_id} | Updates the name of a chat session.
[**update_chat_session_collection**](ChatApi.md#update_chat_session_collection) | **PUT** /chats/{session_id}/collection | Updates a collection reference of a chat session.
[**update_chat_session_prompt_template**](ChatApi.md#update_chat_session_prompt_template) | **PUT** /chats/{session_id}/prompt_template | Updates a prompt template reference of a chat session.


# **create_chat_session**
> ChatSession create_chat_session(collection_id=collection_id)

Creates chat session.

Creates chat session with a collection if provided. Otherwise, the session will be with a generic LLM.

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
    api_instance = h2ogpte_rest_client.ChatApi(api_client)
    collection_id = 'collection_id_example' # str | Id of collection (optional)

    try:
        # Creates chat session.
        api_response = api_instance.create_chat_session(collection_id=collection_id)
        print("The response of ChatApi->create_chat_session:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChatApi->create_chat_session: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Id of collection | [optional] 

### Return type

[**ChatSession**](ChatSession.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful operation |  -  |
**401** | Unauthorized - Invalid or missing API key |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_chat_session**
> ChatSession delete_chat_session(session_id, timeout=timeout)

Deletes collection.

Deletes collection with a given unique identifier.

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
    api_instance = h2ogpte_rest_client.ChatApi(api_client)
    session_id = 'session_id_example' # str | Id of the chat session
    timeout = 300 # int | Timeout in seconds (optional) (default to 300)

    try:
        # Deletes collection.
        api_response = api_instance.delete_chat_session(session_id, timeout=timeout)
        print("The response of ChatApi->delete_chat_session:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChatApi->delete_chat_session: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**| Id of the chat session | 
 **timeout** | **int**| Timeout in seconds | [optional] [default to 300]

### Return type

[**ChatSession**](ChatSession.md)

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

# **delete_chat_session_collection**
> ChatSession delete_chat_session_collection(session_id)

Removes a collection reference from the chat session.

Removes a collection reference from the chat session.

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
    api_instance = h2ogpte_rest_client.ChatApi(api_client)
    session_id = 'session_id_example' # str | Id of the chat session

    try:
        # Removes a collection reference from the chat session.
        api_response = api_instance.delete_chat_session_collection(session_id)
        print("The response of ChatApi->delete_chat_session_collection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChatApi->delete_chat_session_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**| Id of the chat session | 

### Return type

[**ChatSession**](ChatSession.md)

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

# **delete_chat_session_prompt_template**
> ChatSession delete_chat_session_prompt_template(session_id)

Removes a prompt template reference from the chat session.

Removes a prompt template reference from the chat session.

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
    api_instance = h2ogpte_rest_client.ChatApi(api_client)
    session_id = 'session_id_example' # str | Id of the chat session

    try:
        # Removes a prompt template reference from the chat session.
        api_response = api_instance.delete_chat_session_prompt_template(session_id)
        print("The response of ChatApi->delete_chat_session_prompt_template:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChatApi->delete_chat_session_prompt_template: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**| Id of the chat session | 

### Return type

[**ChatSession**](ChatSession.md)

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

# **get_chat_session**
> ChatSession get_chat_session(session_id)

Finds a chat session by id.

Returns a single chat session by its unique identifier.

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
    api_instance = h2ogpte_rest_client.ChatApi(api_client)
    session_id = 'session_id_example' # str | Id of the chat session

    try:
        # Finds a chat session by id.
        api_response = api_instance.get_chat_session(session_id)
        print("The response of ChatApi->get_chat_session:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChatApi->get_chat_session: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**| Id of the chat session | 

### Return type

[**ChatSession**](ChatSession.md)

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

# **get_chat_session_count**
> Count get_chat_session_count()

Counts a number of chat sessions.

Counts a number of chat sessions.

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
    api_instance = h2ogpte_rest_client.ChatApi(api_client)

    try:
        # Counts a number of chat sessions.
        api_response = api_instance.get_chat_session_count()
        print("The response of ChatApi->get_chat_session_count:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChatApi->get_chat_session_count: %s\n" % e)
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

# **get_chat_session_messages**
> List[ChatMessage] get_chat_session_messages(session_id, offset=offset, limit=limit)

Fetches chat message and metadata for messages in a chat session.

Fetches chat message and metadata for messages in a chat session. Messages without a `reply_to` are from the end user, messages with a `reply_to` are from an LLM and a response to a specific user message.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.chat_message import ChatMessage
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
    api_instance = h2ogpte_rest_client.ChatApi(api_client)
    session_id = 'session_id_example' # str | Id of the chat session
    offset = 0 # int | How many chat sessions to skip before returning. (optional) (default to 0)
    limit = 100 # int | How many chat sessions to return. (optional) (default to 100)

    try:
        # Fetches chat message and metadata for messages in a chat session.
        api_response = api_instance.get_chat_session_messages(session_id, offset=offset, limit=limit)
        print("The response of ChatApi->get_chat_session_messages:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChatApi->get_chat_session_messages: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**| Id of the chat session | 
 **offset** | **int**| How many chat sessions to skip before returning. | [optional] [default to 0]
 **limit** | **int**| How many chat sessions to return. | [optional] [default to 100]

### Return type

[**List[ChatMessage]**](ChatMessage.md)

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

# **get_completion**
> ChatCompletion get_completion(session_id, chat_completion_request)



Asks question in a given chat session.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.chat_completion import ChatCompletion
from h2ogpte_rest_client.models.chat_completion_request import ChatCompletionRequest
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
    api_instance = h2ogpte_rest_client.ChatApi(api_client)
    session_id = 'session_id_example' # str | Id of a chat session
    chat_completion_request = h2ogpte_rest_client.ChatCompletionRequest() # ChatCompletionRequest | 

    try:
        api_response = api_instance.get_completion(session_id, chat_completion_request)
        print("The response of ChatApi->get_completion:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChatApi->get_completion: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**| Id of a chat session | 
 **chat_completion_request** | [**ChatCompletionRequest**](ChatCompletionRequest.md)|  | 

### Return type

[**ChatCompletion**](ChatCompletion.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/jsonl

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful operation |  -  |
**401** | Unauthorized - Invalid or missing API key |  -  |
**500** | Internal server error |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_message_meta**
> List[ChatMessageMeta] get_message_meta(message_id, info_type=info_type)

Fetches chat message meta information.

Fetches chat message meta information.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.chat_message_meta import ChatMessageMeta
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
    api_instance = h2ogpte_rest_client.ChatApi(api_client)
    message_id = 'message_id_example' # str | Id of the chat message.
    info_type = 'info_type_example' # str | Metadata type to fetch. (optional)

    try:
        # Fetches chat message meta information.
        api_response = api_instance.get_message_meta(message_id, info_type=info_type)
        print("The response of ChatApi->get_message_meta:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChatApi->get_message_meta: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **message_id** | **str**| Id of the chat message. | 
 **info_type** | **str**| Metadata type to fetch. | [optional] 

### Return type

[**List[ChatMessageMeta]**](ChatMessageMeta.md)

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

# **get_message_references**
> List[ChatMessageReference] get_message_references(message_id)

Fetches metadata for references of a chat message.

Fetches metadata for references of a chat message. References are only available for messages sent from an LLM, an empty list will be returned for messages sent by the user.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.chat_message_reference import ChatMessageReference
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
    api_instance = h2ogpte_rest_client.ChatApi(api_client)
    message_id = 'message_id_example' # str | Id of the chat message

    try:
        # Fetches metadata for references of a chat message.
        api_response = api_instance.get_message_references(message_id)
        print("The response of ChatApi->get_message_references:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChatApi->get_message_references: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **message_id** | **str**| Id of the chat message | 

### Return type

[**List[ChatMessageReference]**](ChatMessageReference.md)

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

# **list_chat_sessions**
> List[ChatSession] list_chat_sessions(offset=offset, limit=limit)

List chat sessions.

List chat sessions.

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
    api_instance = h2ogpte_rest_client.ChatApi(api_client)
    offset = 0 # int | How many chat sessions to skip before returning. (optional) (default to 0)
    limit = 100 # int | How many chat sessions to return. (optional) (default to 100)

    try:
        # List chat sessions.
        api_response = api_instance.list_chat_sessions(offset=offset, limit=limit)
        print("The response of ChatApi->list_chat_sessions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChatApi->list_chat_sessions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
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

# **list_questions_for_chat_session**
> List[SuggestedQuestion] list_questions_for_chat_session(session_id, limit=limit)

List suggested questions for a given chat session.

List suggested questions for a given chat session.

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
    api_instance = h2ogpte_rest_client.ChatApi(api_client)
    session_id = 'session_id_example' # str | Id of a chat session
    limit = 100 # int | How many questions to return. (optional) (default to 100)

    try:
        # List suggested questions for a given chat session.
        api_response = api_instance.list_questions_for_chat_session(session_id, limit=limit)
        print("The response of ChatApi->list_questions_for_chat_session:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChatApi->list_questions_for_chat_session: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**| Id of a chat session | 
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

# **update_chat_session**
> ChatSession update_chat_session(session_id, chat_session_update_request=chat_session_update_request)

Updates the name of a chat session.

Updates the name of a chat session.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.chat_session import ChatSession
from h2ogpte_rest_client.models.chat_session_update_request import ChatSessionUpdateRequest
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
    api_instance = h2ogpte_rest_client.ChatApi(api_client)
    session_id = 'session_id_example' # str | Id of the chat session
    chat_session_update_request = h2ogpte_rest_client.ChatSessionUpdateRequest() # ChatSessionUpdateRequest |  (optional)

    try:
        # Updates the name of a chat session.
        api_response = api_instance.update_chat_session(session_id, chat_session_update_request=chat_session_update_request)
        print("The response of ChatApi->update_chat_session:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChatApi->update_chat_session: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**| Id of the chat session | 
 **chat_session_update_request** | [**ChatSessionUpdateRequest**](ChatSessionUpdateRequest.md)|  | [optional] 

### Return type

[**ChatSession**](ChatSession.md)

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

# **update_chat_session_collection**
> ChatSession update_chat_session_collection(session_id, collection_change_request)

Updates a collection reference of a chat session.

Updates a collection reference of a chat session.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.chat_session import ChatSession
from h2ogpte_rest_client.models.collection_change_request import CollectionChangeRequest
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
    api_instance = h2ogpte_rest_client.ChatApi(api_client)
    session_id = 'session_id_example' # str | Id of the chat session
    collection_change_request = h2ogpte_rest_client.CollectionChangeRequest() # CollectionChangeRequest | 

    try:
        # Updates a collection reference of a chat session.
        api_response = api_instance.update_chat_session_collection(session_id, collection_change_request)
        print("The response of ChatApi->update_chat_session_collection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChatApi->update_chat_session_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**| Id of the chat session | 
 **collection_change_request** | [**CollectionChangeRequest**](CollectionChangeRequest.md)|  | 

### Return type

[**ChatSession**](ChatSession.md)

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

# **update_chat_session_prompt_template**
> ChatSession update_chat_session_prompt_template(session_id, prompt_template_change_request)

Updates a prompt template reference of a chat session.

Updates a prompt template reference of a chat session.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.chat_session import ChatSession
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
    api_instance = h2ogpte_rest_client.ChatApi(api_client)
    session_id = 'session_id_example' # str | Id of the chat session
    prompt_template_change_request = h2ogpte_rest_client.PromptTemplateChangeRequest() # PromptTemplateChangeRequest | 

    try:
        # Updates a prompt template reference of a chat session.
        api_response = api_instance.update_chat_session_prompt_template(session_id, prompt_template_change_request)
        print("The response of ChatApi->update_chat_session_prompt_template:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChatApi->update_chat_session_prompt_template: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**| Id of the chat session | 
 **prompt_template_change_request** | [**PromptTemplateChangeRequest**](PromptTemplateChangeRequest.md)|  | 

### Return type

[**ChatSession**](ChatSession.md)

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

