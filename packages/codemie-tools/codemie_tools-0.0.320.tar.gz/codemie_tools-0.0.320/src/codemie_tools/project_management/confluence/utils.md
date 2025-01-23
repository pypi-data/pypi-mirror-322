# Business Description for `utils.py`

This module provides utility functions for interacting with Confluence, which is a collaboration tool used for project management and documentation.

### Key Functions:

- **validate_creds(confluence: Confluence)**: This function validates the credentials provided for accessing Confluence. It checks whether the Confluence URL is set and raises an error if it is not.

### Error Handling:

In case of missing credentials, an error message is logged, and a `ToolException` is raised to indicate that the required Confluence URL is not provided.