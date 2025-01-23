# Business Description for `utils.py`

## Overview

The `utils.py` module in the `src/codemie_tools/project_management/jira` directory provides utility functions for interacting with Jira, specifically for validating Jira credentials using the Atlassian Jira API.

## Functionality

### `validate_jira_creds`

This function is responsible for validating the Jira credentials passed to it. It performs the following checks:
- Ensures that the Jira URL is provided and is not empty.

If the Jira URL is either `None` or an empty string, it logs an error message and raises a `ToolException` indicating that the Jira URL is required.

## Dependencies
- `logging`: Used for logging error messages.
- `atlassian`: Provides the `Jira` class for interacting with the Jira API.
- `langchain_core.tools`: Contains the `ToolException` class, which is raised in case of validation failure.