# GitHub OpenAI Tools

## Overview
The `github_openai_tools.py` module provides a set of tools designed to interact with the GitHub API, enabling various operations related to branches, pull requests, and file management within a GitHub repository. This module utilizes the CodeMie framework and integrates with OpenAI's language models to enhance functionality and automate tasks.

## Classes

### CreateGithubBranchTool
- **Description**: A tool for creating a new branch in a GitHub repository.
- **Methods**:
  - `execute(branch_name: str, *args)`: Creates a new branch using the provided name.

### SetActiveBranchTool
- **Description**: A tool for setting the active branch in a GitHub repository.
- **Methods**:
  - `execute(branch_name: str, *args)`: Sets the specified branch as active.

### ListBranchesTool
- **Description**: A tool for fetching a list of all branches in a GitHub repository.
- **Methods**:
  - `execute(*args)`: Returns a list of branch names.

### CreatePRTool
- **Description**: A tool for creating a new pull request in a GitHub repository.
- **Methods**:
  - `execute(pr_title: str, pr_body: str, base_branch: str, *args)`: Creates a pull request with the specified title and body, targeting the specified base branch.

### DeleteFileTool
- **Description**: A tool for deleting a file in a GitHub repository.
- **Methods**:
  - `execute(file_path: str, commit_message: str, *args)`: Deletes the specified file and records the provided commit message.

### CreateFileTool
- **Description**: A tool for creating a new file in a GitHub repository.
- **Methods**:
  - `execute(file_path: str, file_contents: str, commit_message: str, *args)`: Creates a file with the specified contents and commit message.

### UpdateFileGitHubTool
- **Description**: A tool for updating a file in a GitHub repository.
- **Methods**:
  - `read_file(file_path)`: Reads the content of a specified file.
  - `update_file(file_path, new_content, commit_message)`: Updates the specified file with new content and commit message.

### OpenAIUpdateFileWholeTool
- **Description**: A tool for updating a file's content using OpenAI's language models.
- **Methods**:
  - `update_content(legacy_content, task_details)`: Updates the file content based on the legacy content and task details.

### OpenAIUpdateFileDiffTool
- **Description**: A tool for updating a file's content based on a diff using OpenAI's language models.
- **Methods**:
  - `update_content(legacy_content, task_details)`: Updates the file content based on the legacy content and task details using a diff approach.

## Conclusion
This module encapsulates various functionalities for managing GitHub repositories using the CodeMie framework, enabling users to perform complex Git operations with ease.