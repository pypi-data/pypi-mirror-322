# Keycloak Models

## KeycloakConfig Class

The `KeycloakConfig` class is a Pydantic model used to define the configuration required to connect to a Keycloak server. It ensures that the necessary fields are provided and validated before use.

### Attributes:
- **base_url** (str): The base URL of the Keycloak server.
- **realm** (str): The realm to use for authentication.
- **client_id** (str): The client ID for the application.
- **client_secret** (str): The client secret for the application.

### Validation:
The class includes a model validator that checks for the presence of required fields. If any of the required fields are missing or empty, a `ValueError` is raised with a descriptive message.

### Usage:
To create an instance of `KeycloakConfig`, you must provide values for all the attributes:

```python
config = KeycloakConfig(
    base_url="https://example.com/auth",
    realm="myrealm",
    client_id="myclient",
    client_secret="mysecret"
)
```

This class is crucial for managing Keycloak configurations in applications that integrate with Keycloak for authentication and authorization.