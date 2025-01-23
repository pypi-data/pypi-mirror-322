# GitLab OpenAI Tools

## Overview
This module provides a set of tools that interact with the GitLab API, particularly for performing operations related to branches, pull requests, and file management within GitLab repositories. It leverages the capabilities of the OpenAI language model to enhance these functionalities.

## Classes

### BranchInput
- **Description**: Schema for operations that require a branch name as input.
- **Attributes**:
  - `branch_name`: The name of the branch (e.g. `my_branch`).

### CreateGitLabBranchTool
- **Description**: A tool to create a new branch in the repository using the GitLab API.
- **Methods**:
  - `execute(branch_name)`: Validates the GitLab wrapper and creates a branch with the specified name.

### CreatePRInput
- **Description**: Schema for creating pull requests.
- **Attributes**:
  - `pr_title`: Title of the pull request.
  - `pr_body`: Body or description of the pull request.

### CreatePRTool
- **Description**: A tool to create a new pull request in a GitLab repository.
- **Methods**:
  - `execute(pr_title, pr_body)`: Validates the GitLab wrapper and creates a pull request.

### DeleteFileInput
- **Description**: Schema for file deletion operations.
- **Attributes**:
  - `file_path`: File path of the file to be deleted.
  - `commit_message`: Custom commit message for the deletion.

### DeleteFileTool
- **Description**: A tool to delete a file in a GitLab repository.
- **Methods**:
  - `execute(file_path, commit_message)`: Validates and deletes the specified file.

### CreateFileInput
- **Description**: Schema for creating files in GitLab.
- **Attributes**:
  - `file_path`: Path for the new file to be created.
  - `file_contents`: Content to be added in the new file.
  - `commit_message`: Custom commit message for the creation.

### CreateFileTool
- **Description**: A tool to create a new file in a GitLab repository.
- **Methods**:
  - `execute(file_path, file_contents, commit_message)`: Validates and creates the file with the specified contents.

### SetActiveBranchTool
- **Description**: A tool to set the active branch in the repository.
- **Methods**:
  - `execute(branch_name)`: Validates and sets the active branch.

### ListBranchesTool
- **Description**: A tool to fetch a list of all branches in the GitLab repository.
- **Methods**:
  - `execute()`: Validates and retrieves the list of branches.

### UpdateFileInput
- **Description**: Schema for updating files in GitLab.
- **Attributes**:
  - `file_path`: Path of the file to be updated.
  - `task_details`: Detailed task description for the update.
  - `commit_message`: Custom commit message for the update.

### UpdateFileGitLabTool
- **Description**: A tool for updating files in a GitLab repository.
- **Methods**:
  - `update_content(legacy_content, task_details)`: Updates file content based on task details.

### GetPullRequesChangesInput
- **Description**: Schema for retrieving changes in pull requests.
- **Attributes**:
  - `pr_number`: GitLab Merge Request number.

### GetPullRequesChanges
- **Description**: A tool to get all changes from a pull request in git diff format.
- **Methods**:
  - `execute(pr_number)`: Validates and retrieves changes for the specified pull request.

### CreatePullRequestChangeCommentInput
- **Description**: Schema for adding comments on pull request changes.
- **Attributes**:
  - `pr_number`: GitLab Merge Request number.
  - `file_path`: Path of the changed file.
  - `line_number`: Line number from the diff.
  - `comment`: Comment content.

### CreatePullRequestChangeComment
- **Description**: A tool to create comments on pull request changes.
- **Methods**:
  - `execute(pr_number, file_path, line_number, comment)`: Validates and adds a comment to the specified change.

## Conclusion
This module provides a robust set of tools for developers working with GitLab, enhancing their ability to manage branches, pull requests, and files effectively.