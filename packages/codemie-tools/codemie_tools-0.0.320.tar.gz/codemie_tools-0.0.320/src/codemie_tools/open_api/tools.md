# OpenAPI Tools Module

## Overview
This module provides classes and methods for interacting with OpenAPI specifications and invoking REST APIs.

## Classes

### OpenApiInput
A Pydantic model that validates and structures input for making OpenAPI requests. It contains the following fields:
- **method**: The HTTP method (e.g. GET, POST) to be used for the API request.
- **url**: The URL endpoint of the API.
- **headers**: Optional HTTP headers for the request.
- **fields**: Optional query parameters for the request.
- **body**: Optional JSON body for the request, passed as a string.

### InvokeRestApiBySpec
A class that extends `CodeMieTool`, allowing the execution of REST API calls based on OpenAPI specifications. It includes:
- **openapi_config**: Configuration for OpenAPI, provided during initialization.
- **execute()**: Method that performs the API call, handling headers and request body appropriately.

### GetOpenApiSpec
Another class extending `CodeMieTool`, used to retrieve the OpenAPI specification. It includes:
- **openapi_spec**: The OpenAPI specification to be returned.
- **execute()**: Method to return the stored OpenAPI spec.

## Usage
To use the tools provided in this module, instantiate the `InvokeRestApiBySpec` or `GetOpenApiSpec` classes with the necessary configuration and call their respective methods.