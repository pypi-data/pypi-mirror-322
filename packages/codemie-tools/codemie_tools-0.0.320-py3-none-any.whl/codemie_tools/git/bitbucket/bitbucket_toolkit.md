# Bitbucket Toolkit

This module provides a toolkit for interacting with Bitbucket, allowing users to perform various operations such as creating branches, managing pull requests, and handling files.

## Classes

### BitbucketToolkitUI
- **Description**: UI representation of the Bitbucket toolkit.
- **Attributes**:
  - `toolkit`: Specifies the type of toolkit, which in this case is for Git.
  - `settings_config`: Boolean indicating if settings configuration is enabled.
  - `tools`: A list of tools available in the toolkit including:
    - Set Active Branch
    - Create File
    - Update File
    - Update File Diff
    - Delete File
    - Create Pull Request
    - Create Git Branch
    - List Branches
    - Get Pull Request Changes
    - Create Pull Request Change Comment

### CustomBitbucketToolkit
- **Description**: A custom toolkit for Bitbucket that integrates with Git credentials and the Bitbucket API.
- **Attributes**:
  - `git_creds`: Credentials for Git operations.
  - `api_wrapper`: Optional API wrapper for Bitbucket operations.
  - `llm_model`: Optional language model for operations.

- **Methods**:
  - `get_tools_ui_info`: Returns UI information for the toolkit.
  - `get_toolkit`: Initializes the toolkit with configuration and returns an instance of CustomBitbucketToolkit.
  - `get_tools`: Returns a list of tools available for use in the toolkit.