# h2ogpte_rest_client.ModelsApi

All URIs are relative to *https://h2ogpte.genai.h2o.ai/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_performance_stats_by_model**](ModelsApi.md#get_performance_stats_by_model) | **GET** /stats/performance_by_model | Returns performance statistics grouped by models.
[**get_usage_stats**](ModelsApi.md#get_usage_stats) | **GET** /stats/usage | Returns usage statistics for all models.
[**get_usage_stats_by_model**](ModelsApi.md#get_usage_stats_by_model) | **GET** /stats/usage_by_model | Returns usage statistics grouped by models.
[**get_usage_stats_by_model_and_user**](ModelsApi.md#get_usage_stats_by_model_and_user) | **GET** /stats/usage_by_model_and_user | Returns usage statistics grouped by models and users.
[**get_usage_stats_by_user**](ModelsApi.md#get_usage_stats_by_user) | **GET** /stats/usage_by_user | Returns usage statistics grouped by users.
[**list_models**](ModelsApi.md#list_models) | **GET** /models | Lists all available large language models.


# **get_performance_stats_by_model**
> List[PerformanceStatsPerModel] get_performance_stats_by_model(interval)

Returns performance statistics grouped by models.

Returns performance statistics grouped by models.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.performance_stats_per_model import PerformanceStatsPerModel
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
    api_instance = h2ogpte_rest_client.ModelsApi(api_client)
    interval = '24 hours' # str | The length of an interval for which the stats will be obtained. The interval ends now.

    try:
        # Returns performance statistics grouped by models.
        api_response = api_instance.get_performance_stats_by_model(interval)
        print("The response of ModelsApi->get_performance_stats_by_model:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModelsApi->get_performance_stats_by_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **interval** | **str**| The length of an interval for which the stats will be obtained. The interval ends now. | 

### Return type

[**List[PerformanceStatsPerModel]**](PerformanceStatsPerModel.md)

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

# **get_usage_stats**
> UsageStats get_usage_stats(interval)

Returns usage statistics for all models.

Returns usage statistics for all models.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.usage_stats import UsageStats
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
    api_instance = h2ogpte_rest_client.ModelsApi(api_client)
    interval = '24 hours' # str | The length of an interval for which the stats will be obtained. The interval ends now.

    try:
        # Returns usage statistics for all models.
        api_response = api_instance.get_usage_stats(interval)
        print("The response of ModelsApi->get_usage_stats:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModelsApi->get_usage_stats: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **interval** | **str**| The length of an interval for which the stats will be obtained. The interval ends now. | 

### Return type

[**UsageStats**](UsageStats.md)

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

# **get_usage_stats_by_model**
> List[UsageStatsPerModel] get_usage_stats_by_model(interval)

Returns usage statistics grouped by models.

Returns usage statistics grouped by models.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.usage_stats_per_model import UsageStatsPerModel
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
    api_instance = h2ogpte_rest_client.ModelsApi(api_client)
    interval = '24 hours' # str | The length of an interval for which the stats will be obtained. The interval ends now.

    try:
        # Returns usage statistics grouped by models.
        api_response = api_instance.get_usage_stats_by_model(interval)
        print("The response of ModelsApi->get_usage_stats_by_model:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModelsApi->get_usage_stats_by_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **interval** | **str**| The length of an interval for which the stats will be obtained. The interval ends now. | 

### Return type

[**List[UsageStatsPerModel]**](UsageStatsPerModel.md)

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

# **get_usage_stats_by_model_and_user**
> List[UsageStatsPerModelAndUser] get_usage_stats_by_model_and_user(interval)

Returns usage statistics grouped by models and users.

Returns usage statistics grouped by models and users.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.usage_stats_per_model_and_user import UsageStatsPerModelAndUser
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
    api_instance = h2ogpte_rest_client.ModelsApi(api_client)
    interval = '24 hours' # str | The length of an interval for which the stats will be obtained. The interval ends now.

    try:
        # Returns usage statistics grouped by models and users.
        api_response = api_instance.get_usage_stats_by_model_and_user(interval)
        print("The response of ModelsApi->get_usage_stats_by_model_and_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModelsApi->get_usage_stats_by_model_and_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **interval** | **str**| The length of an interval for which the stats will be obtained. The interval ends now. | 

### Return type

[**List[UsageStatsPerModelAndUser]**](UsageStatsPerModelAndUser.md)

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

# **get_usage_stats_by_user**
> List[UsageStatsPerUser] get_usage_stats_by_user(interval)

Returns usage statistics grouped by users.

Returns usage statistics grouped by users.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.usage_stats_per_user import UsageStatsPerUser
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
    api_instance = h2ogpte_rest_client.ModelsApi(api_client)
    interval = '24 hours' # str | The length of an interval for which the stats will be obtained. The interval ends now.

    try:
        # Returns usage statistics grouped by users.
        api_response = api_instance.get_usage_stats_by_user(interval)
        print("The response of ModelsApi->get_usage_stats_by_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModelsApi->get_usage_stats_by_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **interval** | **str**| The length of an interval for which the stats will be obtained. The interval ends now. | 

### Return type

[**List[UsageStatsPerUser]**](UsageStatsPerUser.md)

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

# **list_models**
> List[Model] list_models()

Lists all available large language models.

Lists all available large language models.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.model import Model
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
    api_instance = h2ogpte_rest_client.ModelsApi(api_client)

    try:
        # Lists all available large language models.
        api_response = api_instance.list_models()
        print("The response of ModelsApi->list_models:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModelsApi->list_models: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[Model]**](Model.md)

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

