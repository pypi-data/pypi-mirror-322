# OpenApiToolkit Class Description

## Overview
The `OpenApiToolkit` class is a specialized toolkit that extends the `BaseToolkit` for handling OpenAPI specifications and invoking REST APIs based on those specifications.

## Key Components
- **Class Inheritance**: Inherits from `BaseToolkit`.
- **Attributes**:
  - `openapi_config`: An instance of `OpenApiConfig` that holds the configuration for OpenAPI settings.

## Methods
### 1. get_tools_ui_info(cls)
- **Purpose**: Retrieves UI information about the tools available in the toolkit.
- **Returns**: A `ToolKit` object containing the tools and their settings.

### 2. get_tools(self) -> list
- **Purpose**: Returns a list of tools that can be used with the current OpenAPI configuration.
- **Returns**: A list containing instances of the tools `InvokeRestApiBySpec` and `GetOpenApiSpec`.

### 3. get_toolkit(cls, configs: Dict[str, Any] = None)
- **Purpose**: Instantiates the `OpenApiToolkit` with the provided configurations.
- **Parameters**:
  - `configs`: A dictionary containing configuration parameters for the OpenAPI setup.
- **Returns**: An instance of `OpenApiToolkit` initialized with the provided configurations.

## Usage
The `OpenApiToolkit` class is designed to provide essential tools for working with OpenAPI specifications, making it easier to define and manage REST API interactions within the CodeMie platform.