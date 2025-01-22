# h2ogpte_rest_client.PromptTemplatesApi

All URIs are relative to *https://h2ogpte.genai.h2o.ai/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_prompt_template**](PromptTemplatesApi.md#create_prompt_template) | **POST** /prompt_templates | Creates a new prompt template.
[**delete_prompt_template**](PromptTemplatesApi.md#delete_prompt_template) | **DELETE** /prompt_templates/{prompt_template_id} | Deletes a prompt template.
[**get_prompt_template**](PromptTemplatesApi.md#get_prompt_template) | **GET** /prompt_templates/{prompt_template_id} | Finds a prompt template by id.
[**get_prompt_template_count**](PromptTemplatesApi.md#get_prompt_template_count) | **GET** /prompt_templates/count | Counts a number of prompt templates.
[**get_prompt_template_permissions**](PromptTemplatesApi.md#get_prompt_template_permissions) | **GET** /prompt_templates/{prompt_template_id}/permissions | Returns a list of access permissions for a given prompt template.
[**list_prompt_templates**](PromptTemplatesApi.md#list_prompt_templates) | **GET** /prompt_templates | List prompt templates.
[**share_prompt_template**](PromptTemplatesApi.md#share_prompt_template) | **PUT** /prompt_templates/{prompt_template_id}/permissions/{username} | Shares a prompt template to a user.
[**unshare_prompt_template**](PromptTemplatesApi.md#unshare_prompt_template) | **DELETE** /prompt_templates/{prompt_template_id}/permissions/{username} | Removes sharing of a prompt template to a user.
[**unshare_prompt_template_for_all**](PromptTemplatesApi.md#unshare_prompt_template_for_all) | **DELETE** /prompt_templates/{prompt_template_id}/permissions | Removes sharing of a prompt template to all other users except the original owner.
[**update_prompt_template**](PromptTemplatesApi.md#update_prompt_template) | **PATCH** /prompt_templates/{prompt_template_id} | Updates attributes of a given prompt template.


# **create_prompt_template**
> PromptTemplate create_prompt_template(prompt_template_create_request)

Creates a new prompt template.

Creates a new prompt template that can be subsequently associated with a collection.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.prompt_template import PromptTemplate
from h2ogpte_rest_client.models.prompt_template_create_request import PromptTemplateCreateRequest
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
    api_instance = h2ogpte_rest_client.PromptTemplatesApi(api_client)
    prompt_template_create_request = h2ogpte_rest_client.PromptTemplateCreateRequest() # PromptTemplateCreateRequest | 

    try:
        # Creates a new prompt template.
        api_response = api_instance.create_prompt_template(prompt_template_create_request)
        print("The response of PromptTemplatesApi->create_prompt_template:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PromptTemplatesApi->create_prompt_template: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prompt_template_create_request** | [**PromptTemplateCreateRequest**](PromptTemplateCreateRequest.md)|  | 

### Return type

[**PromptTemplate**](PromptTemplate.md)

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

# **delete_prompt_template**
> delete_prompt_template(prompt_template_id)

Deletes a prompt template.

Deletes a prompt template with a given unique identifier.

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
    api_instance = h2ogpte_rest_client.PromptTemplatesApi(api_client)
    prompt_template_id = 'prompt_template_id_example' # str | Id of a prompt template to delete

    try:
        # Deletes a prompt template.
        api_instance.delete_prompt_template(prompt_template_id)
    except Exception as e:
        print("Exception when calling PromptTemplatesApi->delete_prompt_template: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prompt_template_id** | **str**| Id of a prompt template to delete | 

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

# **get_prompt_template**
> PromptTemplate get_prompt_template(prompt_template_id)

Finds a prompt template by id.

Returns a single tag by its unique identifier.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.prompt_template import PromptTemplate
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
    api_instance = h2ogpte_rest_client.PromptTemplatesApi(api_client)
    prompt_template_id = 'prompt_template_id_example' # str | Id of a prompt template to return

    try:
        # Finds a prompt template by id.
        api_response = api_instance.get_prompt_template(prompt_template_id)
        print("The response of PromptTemplatesApi->get_prompt_template:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PromptTemplatesApi->get_prompt_template: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prompt_template_id** | **str**| Id of a prompt template to return | 

### Return type

[**PromptTemplate**](PromptTemplate.md)

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

# **get_prompt_template_count**
> Count get_prompt_template_count()

Counts a number of prompt templates.

Counts a number of prompt templates.

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
    api_instance = h2ogpte_rest_client.PromptTemplatesApi(api_client)

    try:
        # Counts a number of prompt templates.
        api_response = api_instance.get_prompt_template_count()
        print("The response of PromptTemplatesApi->get_prompt_template_count:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PromptTemplatesApi->get_prompt_template_count: %s\n" % e)
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

# **get_prompt_template_permissions**
> List[SharePermission] get_prompt_template_permissions(prompt_template_id)

Returns a list of access permissions for a given prompt template.

The returned list of permissions denotes who has access to the prompt template.

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
    api_instance = h2ogpte_rest_client.PromptTemplatesApi(api_client)
    prompt_template_id = 'prompt_template_id_example' # str | Id of a prompt template

    try:
        # Returns a list of access permissions for a given prompt template.
        api_response = api_instance.get_prompt_template_permissions(prompt_template_id)
        print("The response of PromptTemplatesApi->get_prompt_template_permissions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PromptTemplatesApi->get_prompt_template_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prompt_template_id** | **str**| Id of a prompt template | 

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

# **list_prompt_templates**
> List[PromptTemplate] list_prompt_templates(offset=offset, limit=limit, sort_column=sort_column, ascending=ascending)

List prompt templates.

List all existing prompt templates.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.prompt_template import PromptTemplate
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
    api_instance = h2ogpte_rest_client.PromptTemplatesApi(api_client)
    offset = 0 # int | How many prompt templates to skip before returning. (optional) (default to 0)
    limit = 100 # int | How many prompt templates to return. (optional) (default to 100)
    sort_column = updated_at # str | Sort column. (optional) (default to updated_at)
    ascending = True # bool | When true, returns sorted by sort_column in ascending order. (optional) (default to True)

    try:
        # List prompt templates.
        api_response = api_instance.list_prompt_templates(offset=offset, limit=limit, sort_column=sort_column, ascending=ascending)
        print("The response of PromptTemplatesApi->list_prompt_templates:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PromptTemplatesApi->list_prompt_templates: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **int**| How many prompt templates to skip before returning. | [optional] [default to 0]
 **limit** | **int**| How many prompt templates to return. | [optional] [default to 100]
 **sort_column** | **str**| Sort column. | [optional] [default to updated_at]
 **ascending** | **bool**| When true, returns sorted by sort_column in ascending order. | [optional] [default to True]

### Return type

[**List[PromptTemplate]**](PromptTemplate.md)

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

# **share_prompt_template**
> share_prompt_template(prompt_template_id, username)

Shares a prompt template to a user.

Shares a prompt template to a user.

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
    api_instance = h2ogpte_rest_client.PromptTemplatesApi(api_client)
    prompt_template_id = 'prompt_template_id_example' # str | Id of a prompt template
    username = 'username_example' # str | User name that will obtain access to the prompt template

    try:
        # Shares a prompt template to a user.
        api_instance.share_prompt_template(prompt_template_id, username)
    except Exception as e:
        print("Exception when calling PromptTemplatesApi->share_prompt_template: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prompt_template_id** | **str**| Id of a prompt template | 
 **username** | **str**| User name that will obtain access to the prompt template | 

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

# **unshare_prompt_template**
> unshare_prompt_template(prompt_template_id, username)

Removes sharing of a prompt template to a user.

Removes sharing of a prompt template to a user.

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
    api_instance = h2ogpte_rest_client.PromptTemplatesApi(api_client)
    prompt_template_id = 'prompt_template_id_example' # str | Id of a prompt template
    username = 'username_example' # str | User name that will lose access to the prompt template

    try:
        # Removes sharing of a prompt template to a user.
        api_instance.unshare_prompt_template(prompt_template_id, username)
    except Exception as e:
        print("Exception when calling PromptTemplatesApi->unshare_prompt_template: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prompt_template_id** | **str**| Id of a prompt template | 
 **username** | **str**| User name that will lose access to the prompt template | 

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

# **unshare_prompt_template_for_all**
> unshare_prompt_template_for_all(prompt_template_id)

Removes sharing of a prompt template to all other users except the original owner.

Removes sharing of a prompt template to all other users except the original owner.

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
    api_instance = h2ogpte_rest_client.PromptTemplatesApi(api_client)
    prompt_template_id = 'prompt_template_id_example' # str | Id of a prompt template

    try:
        # Removes sharing of a prompt template to all other users except the original owner.
        api_instance.unshare_prompt_template_for_all(prompt_template_id)
    except Exception as e:
        print("Exception when calling PromptTemplatesApi->unshare_prompt_template_for_all: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prompt_template_id** | **str**| Id of a prompt template | 

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

# **update_prompt_template**
> PromptTemplate update_prompt_template(prompt_template_id, body)

Updates attributes of a given prompt template.

Updates attributes of a given prompt template.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.prompt_template import PromptTemplate
from h2ogpte_rest_client.models.prompt_template_base import PromptTemplateBase
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
    api_instance = h2ogpte_rest_client.PromptTemplatesApi(api_client)
    prompt_template_id = 'prompt_template_id_example' # str | Id of a prompt template to update
    body = h2ogpte_rest_client.PromptTemplateBase() # PromptTemplateBase | 

    try:
        # Updates attributes of a given prompt template.
        api_response = api_instance.update_prompt_template(prompt_template_id, body)
        print("The response of PromptTemplatesApi->update_prompt_template:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PromptTemplatesApi->update_prompt_template: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prompt_template_id** | **str**| Id of a prompt template to update | 
 **body** | **PromptTemplateBase**|  | 

### Return type

[**PromptTemplate**](PromptTemplate.md)

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

