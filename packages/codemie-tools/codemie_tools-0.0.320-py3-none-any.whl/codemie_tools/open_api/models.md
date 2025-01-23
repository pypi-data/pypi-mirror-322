# OpenApiConfig Model

This file contains the definition of the `OpenApiConfig` model.

## Overview

The `OpenApiConfig` class is built using Pydantic's `BaseModel`. It serves as a data model for storing and validating OpenAPI configuration parameters.

## Attributes
- `spec`: A string that holds the OpenAPI specification.
- `api_key`: A string that represents the API key required for authentication.

## Usage

This model can be used to create instances that validate the OpenAPI configuration data, ensuring that all required fields are present and correctly typed.

## Example

```python
api_config = OpenApiConfig(spec="some_spec", api_key="your_api_key")
```