# Keycloak Utilities

## Overview
This module contains utility functions for interacting with Keycloak, an open-source identity and access management solution. The primary function in this module is responsible for obtaining an admin token from the Keycloak server.

## Function: `get_keycloak_admin_token`

### Description
The `get_keycloak_admin_token` function retrieves an access token for administrative operations in Keycloak. This token is essential for authenticating requests to the Keycloak server.

### Parameters
- `config` (KeycloakConfig): An instance of `KeycloakConfig` containing the necessary configuration details to connect to the Keycloak server.

### Returns
- `str`: The access token as a string.

### Workflow
1. Constructs the URL for obtaining the token using the `base_url`, `realm`, `client_id`, and `client_secret` from the provided configuration.
2. Sends a POST request to the Keycloak server with the required payload.
3. Raises an error if the request fails and returns the access token if successful.