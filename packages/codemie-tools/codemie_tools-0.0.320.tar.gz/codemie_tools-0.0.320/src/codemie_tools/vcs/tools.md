# Business Description for VCS Tools

## Overview

The `vcs/tools.py` file contains classes that define tools for interacting with version control systems (VCS) like GitHub and GitLab. The primary focus is to facilitate HTTP requests to the respective APIs using valid JSON input.

## Classes

### JsonInput
A base model that validates JSON input and ensures only valid JSON is processed. It holds the query string which is essential for making API requests.

### GithubTool
- **Name**: `GithubTool`
- **Description**: A tool for interacting with GitHub's REST API.
- **Key Features**:
  - Requires a valid access token for authentication.
  - Executes requests based on provided JSON query inputs.
  - Handles different HTTP methods and returns the response in JSON format.

### GitlabTool
- **Name**: `GitlabTool`
- **Description**: A tool for interacting with GitLab's REST API.
- **Key Features**:
  - Requires a valid access token for authentication.
  - Supports GET and other HTTP requests to interact with GitLab's API.
  - Ensures that all requests are formatted correctly according to GitLab's API specifications.

## Error Handling
Both tools include error handling to log errors when no credentials are found, ensuring that the user is informed about the required credentials to use the tools effectively.

## Conclusion
The `vcs/tools.py` file provides essential classes for seamless interaction with popular VCS platforms, enabling developers to automate and integrate version control functionalities within their applications.