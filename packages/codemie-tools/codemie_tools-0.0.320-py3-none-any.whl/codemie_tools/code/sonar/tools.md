# Business Description for src/codemie_tools/code/sonar/tools.py

## Overview
The `tools.py` module in the `sonar` package of `codemie_tools` contains the implementation of the `SonarTool`, which is designed to interact with the Sonar REST API for managing code quality issues.

## Key Components
1. **SonarToolInput**: A Pydantic model that defines the input schema for the tool, including the required `relative_url` and optional `params`.
   - `relative_url`: This is a mandatory field that specifies the endpoint to interact with Sonar's API, which should begin with '/api/issues/search'.
   - `params`: This optional field allows for passing additional parameters as a JSON string for API requests.

2. **parse_payload_params()**: A helper function to parse the `params` JSON string into a Python dictionary. It raises a `ToolException` if the JSON is invalid.

3. **SonarTool Class**: This class extends `CodeMieTool` and is responsible for executing the API requests to Sonar.
   - **execute()**: This method takes the `relative_url` and `params`, validates the configuration, and performs a GET request to the Sonar API, returning the JSON response.
   - **validate_config()**: Ensures that the necessary configuration is set before making API calls, raising a ValueError if not.

## Usage
The `SonarTool` can be utilized for various operations against the Sonar API, such as searching for issues in a specified project by providing the necessary parameters. The design emphasizes clean code practices by enforcing the inclusion of specific attributes in API requests.