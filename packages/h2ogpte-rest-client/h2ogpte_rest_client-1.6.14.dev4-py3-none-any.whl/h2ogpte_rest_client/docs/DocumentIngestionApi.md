# h2ogpte_rest_client.DocumentIngestionApi

All URIs are relative to *https://h2ogpte.genai.h2o.ai/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**ingest_from_azure_blob_storage**](DocumentIngestionApi.md#ingest_from_azure_blob_storage) | **POST** /ingest/azure_blob_storage | Adds files from the Azure Blob Storage into a collection.
[**ingest_from_file_system**](DocumentIngestionApi.md#ingest_from_file_system) | **POST** /ingest/file_system | Adds files from the local system into a collection.
[**ingest_from_gcs**](DocumentIngestionApi.md#ingest_from_gcs) | **POST** /ingest/gcs | Adds files from the Google Cloud Storage into a collection.
[**ingest_from_plain_text**](DocumentIngestionApi.md#ingest_from_plain_text) | **POST** /ingest/plain_text | Adds plain text to a collection.
[**ingest_from_s3**](DocumentIngestionApi.md#ingest_from_s3) | **POST** /ingest/s3 | Adds files from the AWS S3 storage into a collection.
[**ingest_from_website**](DocumentIngestionApi.md#ingest_from_website) | **POST** /ingest/website | Crawls and ingest a URL into a collection.
[**ingest_upload**](DocumentIngestionApi.md#ingest_upload) | **POST** /uploads/{upload_id}/ingest | Ingest uploaded document
[**upload_file**](DocumentIngestionApi.md#upload_file) | **PUT** /uploads | 


# **ingest_from_azure_blob_storage**
> ingest_from_azure_blob_storage(collection_id, gen_doc_summaries=gen_doc_summaries, gen_doc_questions=gen_doc_questions, audio_input_language=audio_input_language, ocr_model=ocr_model, tesseract_lang=tesseract_lang, keep_tables_as_one_chunk=keep_tables_as_one_chunk, chunk_by_page=chunk_by_page, handwriting_check=handwriting_check, timeout=timeout, ingest_from_azure_blob_storage_request=ingest_from_azure_blob_storage_request)

Adds files from the Azure Blob Storage into a collection.

Adds files from the Azure Blob Storage into a collection.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.ingest_from_azure_blob_storage_request import IngestFromAzureBlobStorageRequest
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
    api_instance = h2ogpte_rest_client.DocumentIngestionApi(api_client)
    collection_id = 'collection_id_example' # str | String id of the collection to add the ingested documents into.
    gen_doc_summaries = False # bool | Whether to auto-generate document summaries (uses LLM). (optional) (default to False)
    gen_doc_questions = False # bool | Whether to auto-generate sample questions for each document (uses LLM). (optional) (default to False)
    audio_input_language = 'auto' # str | Language of audio files. (optional) (default to 'auto')
    ocr_model = 'auto' # str | Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models. docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages. Mississippi works well on handwriting. - `auto` - Automatic will auto-select the best OCR model for every page. - `off` - Disable OCR for speed, but all images will then be skipped (also no image captions will be made). (optional) (default to 'auto')
    tesseract_lang = 'tesseract_lang_example' # str | Which language to use when using ocr_model=\"tesseract\". (optional)
    keep_tables_as_one_chunk = True # bool | When tables are identified by the table parser the table tokens will be kept in a single chunk. (optional)
    chunk_by_page = True # bool | Each page will be a chunk. `keep_tables_as_one_chunk` will be ignored if this is `true`. (optional)
    handwriting_check = True # bool | Check pages for handwriting. Will use specialized models if handwriting is found. (optional)
    timeout = 300 # int | Timeout in seconds (optional) (default to 300)
    ingest_from_azure_blob_storage_request = h2ogpte_rest_client.IngestFromAzureBlobStorageRequest() # IngestFromAzureBlobStorageRequest |  (optional)

    try:
        # Adds files from the Azure Blob Storage into a collection.
        api_instance.ingest_from_azure_blob_storage(collection_id, gen_doc_summaries=gen_doc_summaries, gen_doc_questions=gen_doc_questions, audio_input_language=audio_input_language, ocr_model=ocr_model, tesseract_lang=tesseract_lang, keep_tables_as_one_chunk=keep_tables_as_one_chunk, chunk_by_page=chunk_by_page, handwriting_check=handwriting_check, timeout=timeout, ingest_from_azure_blob_storage_request=ingest_from_azure_blob_storage_request)
    except Exception as e:
        print("Exception when calling DocumentIngestionApi->ingest_from_azure_blob_storage: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| String id of the collection to add the ingested documents into. | 
 **gen_doc_summaries** | **bool**| Whether to auto-generate document summaries (uses LLM). | [optional] [default to False]
 **gen_doc_questions** | **bool**| Whether to auto-generate sample questions for each document (uses LLM). | [optional] [default to False]
 **audio_input_language** | **str**| Language of audio files. | [optional] [default to &#39;auto&#39;]
 **ocr_model** | **str**| Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models. docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages. Mississippi works well on handwriting. - &#x60;auto&#x60; - Automatic will auto-select the best OCR model for every page. - &#x60;off&#x60; - Disable OCR for speed, but all images will then be skipped (also no image captions will be made). | [optional] [default to &#39;auto&#39;]
 **tesseract_lang** | **str**| Which language to use when using ocr_model&#x3D;\&quot;tesseract\&quot;. | [optional] 
 **keep_tables_as_one_chunk** | **bool**| When tables are identified by the table parser the table tokens will be kept in a single chunk. | [optional] 
 **chunk_by_page** | **bool**| Each page will be a chunk. &#x60;keep_tables_as_one_chunk&#x60; will be ignored if this is &#x60;true&#x60;. | [optional] 
 **handwriting_check** | **bool**| Check pages for handwriting. Will use specialized models if handwriting is found. | [optional] 
 **timeout** | **int**| Timeout in seconds | [optional] [default to 300]
 **ingest_from_azure_blob_storage_request** | [**IngestFromAzureBlobStorageRequest**](IngestFromAzureBlobStorageRequest.md)|  | [optional] 

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

# **ingest_from_file_system**
> ingest_from_file_system(collection_id, ingest_from_file_system_request, gen_doc_summaries=gen_doc_summaries, gen_doc_questions=gen_doc_questions, audio_input_language=audio_input_language, ocr_model=ocr_model, tesseract_lang=tesseract_lang, keep_tables_as_one_chunk=keep_tables_as_one_chunk, chunk_by_page=chunk_by_page, handwriting_check=handwriting_check, timeout=timeout)

Adds files from the local system into a collection.

Adds files from the local system into a collection.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.ingest_from_file_system_request import IngestFromFileSystemRequest
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
    api_instance = h2ogpte_rest_client.DocumentIngestionApi(api_client)
    collection_id = 'collection_id_example' # str | String id of the collection to add the ingested documents into.
    ingest_from_file_system_request = h2ogpte_rest_client.IngestFromFileSystemRequest() # IngestFromFileSystemRequest | 
    gen_doc_summaries = False # bool | Whether to auto-generate document summaries (uses LLM). (optional) (default to False)
    gen_doc_questions = False # bool | Whether to auto-generate sample questions for each document (uses LLM). (optional) (default to False)
    audio_input_language = 'auto' # str | Language of audio files. (optional) (default to 'auto')
    ocr_model = 'auto' # str | Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models. docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages. Mississippi works well on handwriting. - `auto` - Automatic will auto-select the best OCR model for every page. - `off` - Disable OCR for speed, but all images will then be skipped (also no image captions will be made). (optional) (default to 'auto')
    tesseract_lang = 'tesseract_lang_example' # str | Which language to use when using ocr_model=\"tesseract\". (optional)
    keep_tables_as_one_chunk = True # bool | When tables are identified by the table parser the table tokens will be kept in a single chunk. (optional)
    chunk_by_page = True # bool | Each page will be a chunk. `keep_tables_as_one_chunk` will be ignored if this is `true`. (optional)
    handwriting_check = True # bool | Check pages for handwriting. Will use specialized models if handwriting is found. (optional)
    timeout = 300 # int | Timeout in seconds (optional) (default to 300)

    try:
        # Adds files from the local system into a collection.
        api_instance.ingest_from_file_system(collection_id, ingest_from_file_system_request, gen_doc_summaries=gen_doc_summaries, gen_doc_questions=gen_doc_questions, audio_input_language=audio_input_language, ocr_model=ocr_model, tesseract_lang=tesseract_lang, keep_tables_as_one_chunk=keep_tables_as_one_chunk, chunk_by_page=chunk_by_page, handwriting_check=handwriting_check, timeout=timeout)
    except Exception as e:
        print("Exception when calling DocumentIngestionApi->ingest_from_file_system: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| String id of the collection to add the ingested documents into. | 
 **ingest_from_file_system_request** | [**IngestFromFileSystemRequest**](IngestFromFileSystemRequest.md)|  | 
 **gen_doc_summaries** | **bool**| Whether to auto-generate document summaries (uses LLM). | [optional] [default to False]
 **gen_doc_questions** | **bool**| Whether to auto-generate sample questions for each document (uses LLM). | [optional] [default to False]
 **audio_input_language** | **str**| Language of audio files. | [optional] [default to &#39;auto&#39;]
 **ocr_model** | **str**| Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models. docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages. Mississippi works well on handwriting. - &#x60;auto&#x60; - Automatic will auto-select the best OCR model for every page. - &#x60;off&#x60; - Disable OCR for speed, but all images will then be skipped (also no image captions will be made). | [optional] [default to &#39;auto&#39;]
 **tesseract_lang** | **str**| Which language to use when using ocr_model&#x3D;\&quot;tesseract\&quot;. | [optional] 
 **keep_tables_as_one_chunk** | **bool**| When tables are identified by the table parser the table tokens will be kept in a single chunk. | [optional] 
 **chunk_by_page** | **bool**| Each page will be a chunk. &#x60;keep_tables_as_one_chunk&#x60; will be ignored if this is &#x60;true&#x60;. | [optional] 
 **handwriting_check** | **bool**| Check pages for handwriting. Will use specialized models if handwriting is found. | [optional] 
 **timeout** | **int**| Timeout in seconds | [optional] [default to 300]

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

# **ingest_from_gcs**
> ingest_from_gcs(collection_id, ingest_from_gcs_request, gen_doc_summaries=gen_doc_summaries, gen_doc_questions=gen_doc_questions, audio_input_language=audio_input_language, ocr_model=ocr_model, tesseract_lang=tesseract_lang, keep_tables_as_one_chunk=keep_tables_as_one_chunk, chunk_by_page=chunk_by_page, handwriting_check=handwriting_check, timeout=timeout)

Adds files from the Google Cloud Storage into a collection.

Adds files from the Google Cloud Storage into a collection.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.ingest_from_gcs_request import IngestFromGcsRequest
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
    api_instance = h2ogpte_rest_client.DocumentIngestionApi(api_client)
    collection_id = 'collection_id_example' # str | String id of the collection to add the ingested documents into.
    ingest_from_gcs_request = h2ogpte_rest_client.IngestFromGcsRequest() # IngestFromGcsRequest | 
    gen_doc_summaries = False # bool | Whether to auto-generate document summaries (uses LLM). (optional) (default to False)
    gen_doc_questions = False # bool | Whether to auto-generate sample questions for each document (uses LLM). (optional) (default to False)
    audio_input_language = 'auto' # str | Language of audio files. (optional) (default to 'auto')
    ocr_model = 'auto' # str | Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models. docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages. Mississippi works well on handwriting. - `auto` - Automatic will auto-select the best OCR model for every page. - `off` - Disable OCR for speed, but all images will then be skipped (also no image captions will be made). (optional) (default to 'auto')
    tesseract_lang = 'tesseract_lang_example' # str | Which language to use when using ocr_model=\"tesseract\". (optional)
    keep_tables_as_one_chunk = True # bool | When tables are identified by the table parser the table tokens will be kept in a single chunk. (optional)
    chunk_by_page = True # bool | Each page will be a chunk. `keep_tables_as_one_chunk` will be ignored if this is `true`. (optional)
    handwriting_check = True # bool | Check pages for handwriting. Will use specialized models if handwriting is found. (optional)
    timeout = 300 # int | Timeout in seconds (optional) (default to 300)

    try:
        # Adds files from the Google Cloud Storage into a collection.
        api_instance.ingest_from_gcs(collection_id, ingest_from_gcs_request, gen_doc_summaries=gen_doc_summaries, gen_doc_questions=gen_doc_questions, audio_input_language=audio_input_language, ocr_model=ocr_model, tesseract_lang=tesseract_lang, keep_tables_as_one_chunk=keep_tables_as_one_chunk, chunk_by_page=chunk_by_page, handwriting_check=handwriting_check, timeout=timeout)
    except Exception as e:
        print("Exception when calling DocumentIngestionApi->ingest_from_gcs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| String id of the collection to add the ingested documents into. | 
 **ingest_from_gcs_request** | [**IngestFromGcsRequest**](IngestFromGcsRequest.md)|  | 
 **gen_doc_summaries** | **bool**| Whether to auto-generate document summaries (uses LLM). | [optional] [default to False]
 **gen_doc_questions** | **bool**| Whether to auto-generate sample questions for each document (uses LLM). | [optional] [default to False]
 **audio_input_language** | **str**| Language of audio files. | [optional] [default to &#39;auto&#39;]
 **ocr_model** | **str**| Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models. docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages. Mississippi works well on handwriting. - &#x60;auto&#x60; - Automatic will auto-select the best OCR model for every page. - &#x60;off&#x60; - Disable OCR for speed, but all images will then be skipped (also no image captions will be made). | [optional] [default to &#39;auto&#39;]
 **tesseract_lang** | **str**| Which language to use when using ocr_model&#x3D;\&quot;tesseract\&quot;. | [optional] 
 **keep_tables_as_one_chunk** | **bool**| When tables are identified by the table parser the table tokens will be kept in a single chunk. | [optional] 
 **chunk_by_page** | **bool**| Each page will be a chunk. &#x60;keep_tables_as_one_chunk&#x60; will be ignored if this is &#x60;true&#x60;. | [optional] 
 **handwriting_check** | **bool**| Check pages for handwriting. Will use specialized models if handwriting is found. | [optional] 
 **timeout** | **int**| Timeout in seconds | [optional] [default to 300]

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

# **ingest_from_plain_text**
> ingest_from_plain_text(collection_id, file_name, body, gen_doc_summaries=gen_doc_summaries, gen_doc_questions=gen_doc_questions, timeout=timeout)

Adds plain text to a collection.

Adds plain text to a collection.

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
    api_instance = h2ogpte_rest_client.DocumentIngestionApi(api_client)
    collection_id = 'collection_id_example' # str | String id of the collection to add the ingested documents into.
    file_name = 'file_name_example' # str | String of the file name to use for the document.
    body = 'body_example' # str | The text that will ingested into a collection.
    gen_doc_summaries = False # bool | Whether to auto-generate document summaries (uses LLM). (optional) (default to False)
    gen_doc_questions = False # bool | Whether to auto-generate sample questions for each document (uses LLM). (optional) (default to False)
    timeout = 300 # int | Timeout in seconds (optional) (default to 300)

    try:
        # Adds plain text to a collection.
        api_instance.ingest_from_plain_text(collection_id, file_name, body, gen_doc_summaries=gen_doc_summaries, gen_doc_questions=gen_doc_questions, timeout=timeout)
    except Exception as e:
        print("Exception when calling DocumentIngestionApi->ingest_from_plain_text: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| String id of the collection to add the ingested documents into. | 
 **file_name** | **str**| String of the file name to use for the document. | 
 **body** | **str**| The text that will ingested into a collection. | 
 **gen_doc_summaries** | **bool**| Whether to auto-generate document summaries (uses LLM). | [optional] [default to False]
 **gen_doc_questions** | **bool**| Whether to auto-generate sample questions for each document (uses LLM). | [optional] [default to False]
 **timeout** | **int**| Timeout in seconds | [optional] [default to 300]

### Return type

void (empty response body)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: text/plain
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful operation |  -  |
**401** | Unauthorized - Invalid or missing API key |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ingest_from_s3**
> ingest_from_s3(collection_id, ingest_from_s3_request, gen_doc_summaries=gen_doc_summaries, gen_doc_questions=gen_doc_questions, audio_input_language=audio_input_language, ocr_model=ocr_model, tesseract_lang=tesseract_lang, keep_tables_as_one_chunk=keep_tables_as_one_chunk, chunk_by_page=chunk_by_page, handwriting_check=handwriting_check, timeout=timeout)

Adds files from the AWS S3 storage into a collection.

Adds files from the AWS S3 storage into a collection.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.ingest_from_s3_request import IngestFromS3Request
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
    api_instance = h2ogpte_rest_client.DocumentIngestionApi(api_client)
    collection_id = 'collection_id_example' # str | String id of the collection to add the ingested documents into.
    ingest_from_s3_request = h2ogpte_rest_client.IngestFromS3Request() # IngestFromS3Request | 
    gen_doc_summaries = False # bool | Whether to auto-generate document summaries (uses LLM). (optional) (default to False)
    gen_doc_questions = False # bool | Whether to auto-generate sample questions for each document (uses LLM). (optional) (default to False)
    audio_input_language = 'auto' # str | Language of audio files. (optional) (default to 'auto')
    ocr_model = 'auto' # str | Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models. docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages. Mississippi works well on handwriting. - `auto` - Automatic will auto-select the best OCR model for every page. - `off` - Disable OCR for speed, but all images will then be skipped (also no image captions will be made). (optional) (default to 'auto')
    tesseract_lang = 'tesseract_lang_example' # str | Which language to use when using ocr_model=\"tesseract\". (optional)
    keep_tables_as_one_chunk = True # bool | When tables are identified by the table parser the table tokens will be kept in a single chunk. (optional)
    chunk_by_page = True # bool | Each page will be a chunk. `keep_tables_as_one_chunk` will be ignored if this is `true`. (optional)
    handwriting_check = True # bool | Check pages for handwriting. Will use specialized models if handwriting is found. (optional)
    timeout = 300 # int | Timeout in seconds (optional) (default to 300)

    try:
        # Adds files from the AWS S3 storage into a collection.
        api_instance.ingest_from_s3(collection_id, ingest_from_s3_request, gen_doc_summaries=gen_doc_summaries, gen_doc_questions=gen_doc_questions, audio_input_language=audio_input_language, ocr_model=ocr_model, tesseract_lang=tesseract_lang, keep_tables_as_one_chunk=keep_tables_as_one_chunk, chunk_by_page=chunk_by_page, handwriting_check=handwriting_check, timeout=timeout)
    except Exception as e:
        print("Exception when calling DocumentIngestionApi->ingest_from_s3: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| String id of the collection to add the ingested documents into. | 
 **ingest_from_s3_request** | [**IngestFromS3Request**](IngestFromS3Request.md)|  | 
 **gen_doc_summaries** | **bool**| Whether to auto-generate document summaries (uses LLM). | [optional] [default to False]
 **gen_doc_questions** | **bool**| Whether to auto-generate sample questions for each document (uses LLM). | [optional] [default to False]
 **audio_input_language** | **str**| Language of audio files. | [optional] [default to &#39;auto&#39;]
 **ocr_model** | **str**| Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models. docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages. Mississippi works well on handwriting. - &#x60;auto&#x60; - Automatic will auto-select the best OCR model for every page. - &#x60;off&#x60; - Disable OCR for speed, but all images will then be skipped (also no image captions will be made). | [optional] [default to &#39;auto&#39;]
 **tesseract_lang** | **str**| Which language to use when using ocr_model&#x3D;\&quot;tesseract\&quot;. | [optional] 
 **keep_tables_as_one_chunk** | **bool**| When tables are identified by the table parser the table tokens will be kept in a single chunk. | [optional] 
 **chunk_by_page** | **bool**| Each page will be a chunk. &#x60;keep_tables_as_one_chunk&#x60; will be ignored if this is &#x60;true&#x60;. | [optional] 
 **handwriting_check** | **bool**| Check pages for handwriting. Will use specialized models if handwriting is found. | [optional] 
 **timeout** | **int**| Timeout in seconds | [optional] [default to 300]

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

# **ingest_from_website**
> ingest_from_website(collection_id, ingest_from_website_request, follow_links=follow_links, max_depth=max_depth, max_documents=max_documents, gen_doc_summaries=gen_doc_summaries, gen_doc_questions=gen_doc_questions, audio_input_language=audio_input_language, ocr_model=ocr_model, tesseract_lang=tesseract_lang, keep_tables_as_one_chunk=keep_tables_as_one_chunk, chunk_by_page=chunk_by_page, handwriting_check=handwriting_check, timeout=timeout)

Crawls and ingest a URL into a collection.

Crawls and ingest a URL into a collection. The web page or document linked from this URL will be imported.

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.ingest_from_website_request import IngestFromWebsiteRequest
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
    api_instance = h2ogpte_rest_client.DocumentIngestionApi(api_client)
    collection_id = 'collection_id_example' # str | String id of the collection to add the ingested documents into.
    ingest_from_website_request = h2ogpte_rest_client.IngestFromWebsiteRequest() # IngestFromWebsiteRequest | 
    follow_links = False # bool | Whether to import all web pages linked from this URL will be imported. External links will be ignored. Links to other pages on the same domain will be followed as long as they are at the same level or below the URL you specify. Each page will be transformed into a PDF document. (optional) (default to False)
    max_depth = -1 # int | Max depth of recursion when following links, only when follow_links is True. Max_depth of 0 means don't follow any links, max_depth of 1 means follow only top-level links, etc. Use -1 for automatic (system settings). (optional) (default to -1)
    max_documents = 56 # int | Max number of documents when following links, only when follow_links is True. Use None for automatic (system defaults). Use -1 for max (system limit). (optional)
    gen_doc_summaries = False # bool | Whether to auto-generate document summaries (uses LLM). (optional) (default to False)
    gen_doc_questions = False # bool | Whether to auto-generate sample questions for each document (uses LLM). (optional) (default to False)
    audio_input_language = 'auto' # str | Language of audio files. (optional) (default to 'auto')
    ocr_model = 'auto' # str | Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models. docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages. Mississippi works well on handwriting. - `auto` - Automatic will auto-select the best OCR model for every page. - `off` - Disable OCR for speed, but all images will then be skipped (also no image captions will be made). (optional) (default to 'auto')
    tesseract_lang = 'tesseract_lang_example' # str | Which language to use when using ocr_model=\"tesseract\". (optional)
    keep_tables_as_one_chunk = True # bool | When tables are identified by the table parser the table tokens will be kept in a single chunk. (optional)
    chunk_by_page = True # bool | Each page will be a chunk. `keep_tables_as_one_chunk` will be ignored if this is `true`. (optional)
    handwriting_check = True # bool | Check pages for handwriting. Will use specialized models if handwriting is found. (optional)
    timeout = 300 # int | Timeout in seconds (optional) (default to 300)

    try:
        # Crawls and ingest a URL into a collection.
        api_instance.ingest_from_website(collection_id, ingest_from_website_request, follow_links=follow_links, max_depth=max_depth, max_documents=max_documents, gen_doc_summaries=gen_doc_summaries, gen_doc_questions=gen_doc_questions, audio_input_language=audio_input_language, ocr_model=ocr_model, tesseract_lang=tesseract_lang, keep_tables_as_one_chunk=keep_tables_as_one_chunk, chunk_by_page=chunk_by_page, handwriting_check=handwriting_check, timeout=timeout)
    except Exception as e:
        print("Exception when calling DocumentIngestionApi->ingest_from_website: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| String id of the collection to add the ingested documents into. | 
 **ingest_from_website_request** | [**IngestFromWebsiteRequest**](IngestFromWebsiteRequest.md)|  | 
 **follow_links** | **bool**| Whether to import all web pages linked from this URL will be imported. External links will be ignored. Links to other pages on the same domain will be followed as long as they are at the same level or below the URL you specify. Each page will be transformed into a PDF document. | [optional] [default to False]
 **max_depth** | **int**| Max depth of recursion when following links, only when follow_links is True. Max_depth of 0 means don&#39;t follow any links, max_depth of 1 means follow only top-level links, etc. Use -1 for automatic (system settings). | [optional] [default to -1]
 **max_documents** | **int**| Max number of documents when following links, only when follow_links is True. Use None for automatic (system defaults). Use -1 for max (system limit). | [optional] 
 **gen_doc_summaries** | **bool**| Whether to auto-generate document summaries (uses LLM). | [optional] [default to False]
 **gen_doc_questions** | **bool**| Whether to auto-generate sample questions for each document (uses LLM). | [optional] [default to False]
 **audio_input_language** | **str**| Language of audio files. | [optional] [default to &#39;auto&#39;]
 **ocr_model** | **str**| Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models. docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages. Mississippi works well on handwriting. - &#x60;auto&#x60; - Automatic will auto-select the best OCR model for every page. - &#x60;off&#x60; - Disable OCR for speed, but all images will then be skipped (also no image captions will be made). | [optional] [default to &#39;auto&#39;]
 **tesseract_lang** | **str**| Which language to use when using ocr_model&#x3D;\&quot;tesseract\&quot;. | [optional] 
 **keep_tables_as_one_chunk** | **bool**| When tables are identified by the table parser the table tokens will be kept in a single chunk. | [optional] 
 **chunk_by_page** | **bool**| Each page will be a chunk. &#x60;keep_tables_as_one_chunk&#x60; will be ignored if this is &#x60;true&#x60;. | [optional] 
 **handwriting_check** | **bool**| Check pages for handwriting. Will use specialized models if handwriting is found. | [optional] 
 **timeout** | **int**| Timeout in seconds | [optional] [default to 300]

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

# **ingest_upload**
> ingest_upload(upload_id, collection_id, gen_doc_summaries=gen_doc_summaries, gen_doc_questions=gen_doc_questions, audio_input_language=audio_input_language, ocr_model=ocr_model, tesseract_lang=tesseract_lang, keep_tables_as_one_chunk=keep_tables_as_one_chunk, chunk_by_page=chunk_by_page, handwriting_check=handwriting_check, timeout=timeout)

Ingest uploaded document

Ingests uploaded document identified to a given collection

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
    api_instance = h2ogpte_rest_client.DocumentIngestionApi(api_client)
    upload_id = 'upload_id_example' # str | Id of uploaded document
    collection_id = 'collection_id_example' # str | String id of the collection to add the ingested documents into.
    gen_doc_summaries = False # bool | Whether to auto-generate document summaries (uses LLM). (optional) (default to False)
    gen_doc_questions = False # bool | Whether to auto-generate sample questions for each document (uses LLM). (optional) (default to False)
    audio_input_language = 'auto' # str | Language of audio files. (optional) (default to 'auto')
    ocr_model = 'auto' # str | Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models. docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages. Mississippi works well on handwriting. - `auto` - Automatic will auto-select the best OCR model for every page. - `off` - Disable OCR for speed, but all images will then be skipped (also no image captions will be made). (optional) (default to 'auto')
    tesseract_lang = 'tesseract_lang_example' # str | Which language to use when using ocr_model=\"tesseract\". (optional)
    keep_tables_as_one_chunk = True # bool | When tables are identified by the table parser the table tokens will be kept in a single chunk. (optional)
    chunk_by_page = True # bool | Each page will be a chunk. `keep_tables_as_one_chunk` will be ignored if this is `true`. (optional)
    handwriting_check = True # bool | Check pages for handwriting. Will use specialized models if handwriting is found. (optional)
    timeout = 300 # int | Timeout in seconds (optional) (default to 300)

    try:
        # Ingest uploaded document
        api_instance.ingest_upload(upload_id, collection_id, gen_doc_summaries=gen_doc_summaries, gen_doc_questions=gen_doc_questions, audio_input_language=audio_input_language, ocr_model=ocr_model, tesseract_lang=tesseract_lang, keep_tables_as_one_chunk=keep_tables_as_one_chunk, chunk_by_page=chunk_by_page, handwriting_check=handwriting_check, timeout=timeout)
    except Exception as e:
        print("Exception when calling DocumentIngestionApi->ingest_upload: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **upload_id** | **str**| Id of uploaded document | 
 **collection_id** | **str**| String id of the collection to add the ingested documents into. | 
 **gen_doc_summaries** | **bool**| Whether to auto-generate document summaries (uses LLM). | [optional] [default to False]
 **gen_doc_questions** | **bool**| Whether to auto-generate sample questions for each document (uses LLM). | [optional] [default to False]
 **audio_input_language** | **str**| Language of audio files. | [optional] [default to &#39;auto&#39;]
 **ocr_model** | **str**| Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models. docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages. Mississippi works well on handwriting. - &#x60;auto&#x60; - Automatic will auto-select the best OCR model for every page. - &#x60;off&#x60; - Disable OCR for speed, but all images will then be skipped (also no image captions will be made). | [optional] [default to &#39;auto&#39;]
 **tesseract_lang** | **str**| Which language to use when using ocr_model&#x3D;\&quot;tesseract\&quot;. | [optional] 
 **keep_tables_as_one_chunk** | **bool**| When tables are identified by the table parser the table tokens will be kept in a single chunk. | [optional] 
 **chunk_by_page** | **bool**| Each page will be a chunk. &#x60;keep_tables_as_one_chunk&#x60; will be ignored if this is &#x60;true&#x60;. | [optional] 
 **handwriting_check** | **bool**| Check pages for handwriting. Will use specialized models if handwriting is found. | [optional] 
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

# **upload_file**
> UploadedFile upload_file(file=file)



Uploads file to H2OGPTe instance

### Example

* Bearer Authentication (bearerAuth):

```python
import h2ogpte_rest_client
from h2ogpte_rest_client.models.uploaded_file import UploadedFile
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
    api_instance = h2ogpte_rest_client.DocumentIngestionApi(api_client)
    file = None # bytearray |  (optional)

    try:
        api_response = api_instance.upload_file(file=file)
        print("The response of DocumentIngestionApi->upload_file:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocumentIngestionApi->upload_file: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **bytearray**|  | [optional] 

### Return type

[**UploadedFile**](UploadedFile.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful operation |  -  |
**401** | Unauthorized - Invalid or missing API key |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

