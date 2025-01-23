# KeycloakTool Class

## Overview
The `KeycloakTool` class is part of the CodeMie toolkit for managing interactions with Keycloak's Admin API. It allows users to perform various actions such as creating, updating, and deleting users in a Keycloak realm.

## Key Features
- **HTTP Method Support:** Supports standard HTTP methods like GET, POST, PUT, DELETE.
- **Dynamic URL Handling:** Constructs the full API URL dynamically based on the base URL and realm provided in the configuration.
- **Token Management:** Automatically retrieves and manages access tokens necessary for authenticating requests to the Keycloak API.

## Classes and Methods
### KeycloakToolInput
- **Attributes:**
  - `method`: The HTTP method to use for the request (GET, POST, PUT, DELETE).
  - `relative_url`: The relative URL of the Keycloak Admin API to call.
  - `params`: Optional parameters for the request.

### KeycloakTool
- **Attributes:**
  - `keycloak_config`: Configuration settings for Keycloak.
  - `name`: The name of the tool.
  - `description`: A short description of the tool.
  - `args_schema`: Schema definition for input arguments.

- **Methods:**
  - `execute(method: str, relative_url: str, params: Optional[str] = '')`: Executes an API call to the Keycloak Admin API based on the provided method and URL.
  - `parse_payload_params(params: Optional[str])`: Converts a string of parameters into a dictionary format suitable for the request.

## Usage
To use this tool, instantiate the `KeycloakTool` class with the appropriate configuration and call the `execute` method with the desired HTTP method and API endpoint.