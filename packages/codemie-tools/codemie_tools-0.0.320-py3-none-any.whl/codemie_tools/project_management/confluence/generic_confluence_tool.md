# Generic Confluence Tool

## Overview
The `GenericConfluenceTool` class is a part of the CodeMie project management tools designed to interact with the Confluence API. It provides methods for making various HTTP requests to the Confluence server using the Atlassian Python API client.

## Imports
- `json`: For handling JSON data.
- `logging`: For logging messages.
- `re`: For regular expression operations.
- `traceback`: For printing stack traces in case of exceptions.
- `JSONDecodeError`: Exception raised for JSON decoding errors.
- `Type`, `Dict`, `Any`, `Optional`: Type hints from the typing module.
- `Confluence`: Main class from the Atlassian library to interact with Confluence.
- `BaseModel`, `Field`: For defining data models using Pydantic.
- `ToolException`: Custom exception for tool errors.
- `markdownify`: To convert HTML to Markdown.
- `CodeMieTool`: Base class for CodeMie tools.
- `GENERIC_CONFLUENCE_TOOL`: Constants related to the generic Confluence tool.
- `validate_creds`: Utility to validate Confluence credentials.

## ConfluenceInput Class
The `ConfluenceInput` class is a Pydantic model that defines the expected input parameters for the Confluence tool:
- `method`: The HTTP method (GET, POST, PUT, DELETE).
- `relative_url`: The relative URI for the Confluence API, which must start with `/rest/...`.
- `params`: Optional JSON string of parameters for the request body or query.

## Methods
### `parse_payload_params`
This function takes optional parameters and attempts to parse them into a dictionary. If the parameters are not valid JSON, it raises a `ToolException`.

### `execute`
This is the main method for executing the API request. It validates credentials, parses parameters, and makes the request using the provided HTTP method and relative URL. It also logs the response for debugging.

### `process_search_response`
This method processes the response from a search operation. If the relative URL matches the search pattern, it converts the response text from HTML to Markdown format.

## Usage
To use the `GenericConfluenceTool`, create an instance of it by passing the necessary credentials and call the `execute` method with the desired HTTP method, the relative URL, and any parameters.