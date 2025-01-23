# Bitbucket OpenAI Tools

## Overview
This module provides various tools for interacting with Bitbucket's API. It includes functionalities for branch management, pull requests, file operations, and more, leveraging the power of OpenAI for content generation and updates.

## Classes

### Class: `BranchInput`
A schema for operations that require a branch name as input.
- **Attributes:**
  - `branch_name`: The name of the branch (e.g., `my_branch`).

### Class: `CreateBitbucketBranchTool`
A tool for creating a branch in Bitbucket.
- **Methods:**
  - `execute`: Validates credentials and creates a new branch.

### Class: `SetActiveBranchTool`
A tool for setting the active branch in Bitbucket.
- **Methods:**
  - `execute`: Validates credentials and sets the specified branch as active.

### Class: `ListBranchesTool`
A tool for listing all branches in Bitbucket.
- **Methods:**
  - `execute`: Validates credentials and retrieves a list of branches.

### Class: `CreatePRInput`
A schema for creating pull requests.
- **Attributes:**
  - `pr_title`: Title of the pull request.
  - `pr_body`: Body or description of the pull request.
  - `source_branch`: Source branch of the pull request.

### Class: `CreatePRTool`
A tool for creating pull requests in Bitbucket.
- **Methods:**
  - `execute`: Validates credentials and creates a pull request.

### Class: `DeleteFileInput`
A schema for deleting files in Bitbucket.
- **Attributes:**
  - `file_path`: File path of the file to delete.
  - `commit_message`: Commit message for the deletion.

### Class: `DeleteFileTool`
A tool for deleting files in Bitbucket.
- **Methods:**
  - `execute`: Validates credentials and deletes the specified file.

### Class: `CreateFileInput`
A schema for creating files in Bitbucket.
- **Attributes:**
  - `file_path`: File path of the file to create.
  - `file_contents`: Full content of the new file.
  - `commit_message`: Commit message for the creation.

### Class: `CreateFileTool`
A tool for creating files in Bitbucket.
- **Methods:**
  - `execute`: Validates credentials and creates a new file with specified content.

### Class: `UpdateFileInput`
A schema for updating files in Bitbucket.
- **Attributes:**
  - `file_path`: File path of the file to update.
  - `task_details`: Details of the task for the update.
  - `commit_message`: Commit message for the update.

### Class: `UpdateFileBitbucketTool`
A tool for updating files in Bitbucket.
- **Methods:**
  - `read_file`: Reads the content of a specified file.
  - `update_file`: Updates the specified file with new content.

### Class: `OpenAIUpdateFileWholeTool`
A tool for updating files using OpenAI's LLM model.
- **Methods:**
  - `update_content`: Invokes OpenAI to generate updated content based on the task.

### Class: `OpenAIUpdateFileDiffTool`
A tool for updating files based on differences using OpenAI's LLM model.
- **Methods:**
  - `update_content`: Utilizes the `update_content_by_task` function to generate updates.

### Class: `GetPullRequestChanges`
A tool for retrieving changes from a pull request.
- **Methods:**
  - `execute`: Validates credentials and fetches changes from a specified pull request.

### Class: `CreatePullRequestChangeComment`
A tool for adding comments to pull request changes.
- **Methods:**
  - `execute`: Validates credentials and adds a comment to a specified pull request change.

## Conclusion
These tools provide essential functionalities for managing branches, pull requests, and files in Bitbucket, integrated with OpenAI capabilities to enhance content management and automation.