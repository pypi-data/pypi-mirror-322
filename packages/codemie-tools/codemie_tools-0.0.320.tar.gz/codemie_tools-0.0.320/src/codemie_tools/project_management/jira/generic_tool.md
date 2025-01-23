# Generic Jira Issue Tool

## Overview
The `GenericJiraIssueTool` class is a part of the CodeMie project management tools specifically designed for interacting with Jira's REST API. This tool allows for various operations on Jira issues using standard HTTP methods.

## Key Features
- Supports common HTTP methods: GET, POST, PUT, DELETE.
- Validates Jira credentials before making requests.
- Handles parsing of response data and error management.

## Components
### Classes
- **JiraInput**: A Pydantic model that defines the input structure for the Jira requests. It includes fields for:
  - `method`: The HTTP method to use for the request.
  - `relative_url`: The relative URI for Jira's REST API.
  - `params`: Optional parameters for the request, formatted as a JSON string.

### Methods
- **`parse_payload_params(params: Optional[str]) -> Dict[str, Any]`**: Parses the parameters passed to the Jira request, ensuring they are valid JSON.
- **`get_issue_field(issue, field, default=None)`**: Retrieves a specific field from a Jira issue, returning a default value if not found.
- **`process_issue(jira_base_url, issue, payload_params: Dict[str, Any] = None)`**: Processes a Jira issue, extracting relevant fields and creating a structured representation.
- **`execute(method: str, relative_url: str, params: Optional[str] = '', *args)`**: Executes the HTTP request to the Jira API and processes the response.

## Usage
To use the `GenericJiraIssueTool`, instantiate it with a valid Jira client and invoke the `execute` method with the desired HTTP method, relative URL, and parameters. It’s designed to handle both issue retrieval and updates effectively.

## Logging
The tool includes logging capabilities to track HTTP requests and responses, aiding in debugging and monitoring interactions with the Jira API.

## Error Handling
The tool raises exceptions for invalid JSON parameters and includes error logging for failed API requests.