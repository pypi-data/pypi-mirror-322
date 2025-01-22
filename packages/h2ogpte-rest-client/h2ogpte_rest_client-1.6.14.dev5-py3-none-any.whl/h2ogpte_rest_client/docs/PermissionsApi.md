# h2ogpte_rest_client.PermissionsApi

All URIs are relative to *https://h2ogpte.genai.h2o.ai/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**assign_permission_to_role**](PermissionsApi.md#assign_permission_to_role) | **PUT** /roles/{role_id}/permissions/{permission_name} | Assigns permission to a given role.
[**assign_role_to_user**](PermissionsApi.md#assign_role_to_user) | **PUT** /users/{user_id}/roles/{role_name} | Assigns role to a given user.
[**create_role**](PermissionsApi.md#create_role) | **POST** /roles | Creates a role.
[**delete_role**](PermissionsApi.md#delete_role) | **DELETE** /roles/{role_id} | Deletes role for a given unique identifier.
[**get_current_user_permissions**](PermissionsApi.md#get_current_user_permissions) | **GET** /users/current/permissions | Lists permissions of the user calling the endpoint.
[**get_current_user_roles**](PermissionsApi.md#get_current_user_roles) | **GET** /users/current/roles | Finds roles associated with the user calling the endpoint.
[**get_role**](PermissionsApi.md#get_role) | **GET** /roles/{role_id} | Finds role for a given unique identifier.
[**get_role_permissions**](PermissionsApi.md#get_role_permissions) | **GET** /roles/{role_id}/permissions | Lists permissions of a given role.
[**get_user**](PermissionsApi.md#get_user) | **GET** /users/{user_id} | Finds user for a given unique identifier.
[**get_user_permissions**](PermissionsApi.md#get_user_permissions) | **GET** /users/{user_id}/permissions | Lists permissions of a given user.
[**get_user_roles**](PermissionsApi.md#get_user_roles) | **GET** /users/{user_id}/roles | Finds roles associated with a given user.
[**list_roles**](PermissionsApi.md#list_roles) | **GET** /roles | Returns all roles for in the H2OGPTe instance.
[**list_users**](PermissionsApi.md#list_users) | **GET** /users | Returns a list of all registered users for the system.
[**remove_permission_from_role**](PermissionsApi.md#remove_permission_from_role) | **DELETE** /roles/{role_id}/permissions/{permission_name} | Removes permission from a given role.
[**remove_role_from_user**](PermissionsApi.md#remove_role_from_user) | **DELETE** /users/{user_id}/roles/{role_name} | Removes role from a given user.


# **assign_permission_to_role**
> assign_permission_to_role(role_id, permission_name)

Assigns permission to a given role.

Assigns permission to a given role.

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
    api_instance = h2ogpte_rest_client.PermissionsApi(api_client)
    role_id = 'role_id_example' # str | The unique identifier of an user.
    permission_name = 'permission_name_example' # str | The permission name.

    try:
        # Assigns permission to a given role.
        api_instance.assign_permission_to_role(role_id, permission_name)
    except Exception as e:
        print("Exception when calling PermissionsApi->assign_permission_to_role: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **role_id** | **str**| The unique identifier of an user. | 
 **permission_name** | **str**| The permission name. | 

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

# **assign_role_to_user**
> assign_role_to_user(user_id, role_name)

Assigns role to a given user.

Assigns role to a given user.

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
    api_instance = h2ogpte_rest_client.PermissionsApi(api_client)
    user_id = 'user_id_example' # str | The unique identifier of an user.
    role_name = 'role_name_example' # str | The role name.

    try:
        # Assigns role to a given user.
        api_instance.assign_role_to_user(user_id, role_name)
    except Exception as e:
        print("Exception when calling PermissionsApi->assign_role_to_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| The unique identifier of an user. | 
 **role_name** | **str**| The role name. | 

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

# **create_role**
> RoleInfo create_role(role_create_request=role_create_request)

Creates a role.

Creates a role.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.role_create_request import RoleCreateRequest
from h2ogpte_rest_client.models.role_info import RoleInfo
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
    api_instance = h2ogpte_rest_client.PermissionsApi(api_client)
    role_create_request = h2ogpte_rest_client.RoleCreateRequest() # RoleCreateRequest |  (optional)

    try:
        # Creates a role.
        api_response = api_instance.create_role(role_create_request=role_create_request)
        print("The response of PermissionsApi->create_role:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PermissionsApi->create_role: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **role_create_request** | [**RoleCreateRequest**](RoleCreateRequest.md)|  | [optional] 

### Return type

[**RoleInfo**](RoleInfo.md)

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

# **delete_role**
> delete_role(role_id)

Deletes role for a given unique identifier.

Deletes role for a given unique identifier.

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
    api_instance = h2ogpte_rest_client.PermissionsApi(api_client)
    role_id = 'role_id_example' # str | The unique identifier of an role.

    try:
        # Deletes role for a given unique identifier.
        api_instance.delete_role(role_id)
    except Exception as e:
        print("Exception when calling PermissionsApi->delete_role: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **role_id** | **str**| The unique identifier of an role. | 

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

# **get_current_user_permissions**
> List[UserPermission] get_current_user_permissions()

Lists permissions of the user calling the endpoint.

Lists permissions of the user calling the endpoint.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.user_permission import UserPermission
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
    api_instance = h2ogpte_rest_client.PermissionsApi(api_client)

    try:
        # Lists permissions of the user calling the endpoint.
        api_response = api_instance.get_current_user_permissions()
        print("The response of PermissionsApi->get_current_user_permissions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PermissionsApi->get_current_user_permissions: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[UserPermission]**](UserPermission.md)

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

# **get_current_user_roles**
> List[RoleInfo] get_current_user_roles()

Finds roles associated with the user calling the endpoint.

Finds roles associated with the user calling the endpoint.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.role_info import RoleInfo
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
    api_instance = h2ogpte_rest_client.PermissionsApi(api_client)

    try:
        # Finds roles associated with the user calling the endpoint.
        api_response = api_instance.get_current_user_roles()
        print("The response of PermissionsApi->get_current_user_roles:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PermissionsApi->get_current_user_roles: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[RoleInfo]**](RoleInfo.md)

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

# **get_role**
> RoleInfo get_role(role_id)

Finds role for a given unique identifier.

Finds role for a given unique identifier.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.role_info import RoleInfo
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
    api_instance = h2ogpte_rest_client.PermissionsApi(api_client)
    role_id = 'role_id_example' # str | The unique identifier of an role.

    try:
        # Finds role for a given unique identifier.
        api_response = api_instance.get_role(role_id)
        print("The response of PermissionsApi->get_role:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PermissionsApi->get_role: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **role_id** | **str**| The unique identifier of an role. | 

### Return type

[**RoleInfo**](RoleInfo.md)

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

# **get_role_permissions**
> List[UserPermission] get_role_permissions(role_id)

Lists permissions of a given role.

Lists permissions of a given role.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.user_permission import UserPermission
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
    api_instance = h2ogpte_rest_client.PermissionsApi(api_client)
    role_id = 'role_id_example' # str | The unique identifier of an role.

    try:
        # Lists permissions of a given role.
        api_response = api_instance.get_role_permissions(role_id)
        print("The response of PermissionsApi->get_role_permissions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PermissionsApi->get_role_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **role_id** | **str**| The unique identifier of an role. | 

### Return type

[**List[UserPermission]**](UserPermission.md)

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

# **get_user**
> UserInfo get_user(user_id)

Finds user for a given unique identifier.

Finds user for a given unique identifier.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.user_info import UserInfo
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
    api_instance = h2ogpte_rest_client.PermissionsApi(api_client)
    user_id = 'user_id_example' # str | The unique identifier of an user.

    try:
        # Finds user for a given unique identifier.
        api_response = api_instance.get_user(user_id)
        print("The response of PermissionsApi->get_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PermissionsApi->get_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| The unique identifier of an user. | 

### Return type

[**UserInfo**](UserInfo.md)

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

# **get_user_permissions**
> List[UserPermission] get_user_permissions(user_id)

Lists permissions of a given user.

Lists permissions of a given user.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.user_permission import UserPermission
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
    api_instance = h2ogpte_rest_client.PermissionsApi(api_client)
    user_id = 'user_id_example' # str | The unique identifier of an user.

    try:
        # Lists permissions of a given user.
        api_response = api_instance.get_user_permissions(user_id)
        print("The response of PermissionsApi->get_user_permissions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PermissionsApi->get_user_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| The unique identifier of an user. | 

### Return type

[**List[UserPermission]**](UserPermission.md)

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

# **get_user_roles**
> List[RoleInfo] get_user_roles(user_id)

Finds roles associated with a given user.

Finds roles associated with a given user.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.role_info import RoleInfo
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
    api_instance = h2ogpte_rest_client.PermissionsApi(api_client)
    user_id = 'user_id_example' # str | The unique identifier of an user.

    try:
        # Finds roles associated with a given user.
        api_response = api_instance.get_user_roles(user_id)
        print("The response of PermissionsApi->get_user_roles:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PermissionsApi->get_user_roles: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| The unique identifier of an user. | 

### Return type

[**List[RoleInfo]**](RoleInfo.md)

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

# **list_roles**
> List[RoleInfo] list_roles()

Returns all roles for in the H2OGPTe instance.

Returns all roles for in the H2OGPTe instance.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.role_info import RoleInfo
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
    api_instance = h2ogpte_rest_client.PermissionsApi(api_client)

    try:
        # Returns all roles for in the H2OGPTe instance.
        api_response = api_instance.list_roles()
        print("The response of PermissionsApi->list_roles:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PermissionsApi->list_roles: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[RoleInfo]**](RoleInfo.md)

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

# **list_users**
> List[UserInfo] list_users(offset=offset, limit=limit)

Returns a list of all registered users for the system.

Returns a list of all registered users for the system.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.user_info import UserInfo
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
    api_instance = h2ogpte_rest_client.PermissionsApi(api_client)
    offset = 0 # int | How many collections to skip before returning. (optional) (default to 0)
    limit = 100 # int | How many users to return. (optional) (default to 100)

    try:
        # Returns a list of all registered users for the system.
        api_response = api_instance.list_users(offset=offset, limit=limit)
        print("The response of PermissionsApi->list_users:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PermissionsApi->list_users: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **int**| How many collections to skip before returning. | [optional] [default to 0]
 **limit** | **int**| How many users to return. | [optional] [default to 100]

### Return type

[**List[UserInfo]**](UserInfo.md)

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

# **remove_permission_from_role**
> remove_permission_from_role(role_id, permission_name)

Removes permission from a given role.

Removes permission from a given role.

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
    api_instance = h2ogpte_rest_client.PermissionsApi(api_client)
    role_id = 'role_id_example' # str | The unique identifier of an user.
    permission_name = 'permission_name_example' # str | The permission name.

    try:
        # Removes permission from a given role.
        api_instance.remove_permission_from_role(role_id, permission_name)
    except Exception as e:
        print("Exception when calling PermissionsApi->remove_permission_from_role: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **role_id** | **str**| The unique identifier of an user. | 
 **permission_name** | **str**| The permission name. | 

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

# **remove_role_from_user**
> remove_role_from_user(user_id, role_name)

Removes role from a given user.

Removes role from a given user.

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
    api_instance = h2ogpte_rest_client.PermissionsApi(api_client)
    user_id = 'user_id_example' # str | The unique identifier of an user.
    role_name = 'role_name_example' # str | The role name.

    try:
        # Removes role from a given user.
        api_instance.remove_role_from_user(user_id, role_name)
    except Exception as e:
        print("Exception when calling PermissionsApi->remove_role_from_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| The unique identifier of an user. | 
 **role_name** | **str**| The role name. | 

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

