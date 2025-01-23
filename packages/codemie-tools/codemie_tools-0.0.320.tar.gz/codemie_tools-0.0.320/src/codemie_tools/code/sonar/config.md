# Business Description for SonarToolConfig

The `SonarToolConfig` class is a configuration model for the Sonar tool, used to manage and analyze code quality. It is built using Pydantic, which provides data validation and settings management through Python type annotations.

## Attributes:

- **url (Optional[str])**: This attribute holds the URL of the Sonar server. It is an optional field that can be set to `None` if not applicable.
- **sonar_token (Optional[str])**: This attribute is used to authenticate with the Sonar server. It is essential for secure access and is also optional.
- **sonar_project_name (Optional[str])**: This attribute represents the name of the project in Sonar. It is also optional and can be left as `None` if not specified.

## Usage:

This configuration model allows users to easily set up and manage parameters required for interacting with the Sonar tool, ensuring that necessary fields are validated and correctly formatted.