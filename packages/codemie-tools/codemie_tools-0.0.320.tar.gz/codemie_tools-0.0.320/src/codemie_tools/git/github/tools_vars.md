# GitHub Tools Variables

This document outlines the various tools available for GitHub integration within the CodeMie platform.

## Tools Overview

### Create Git Branch Tool
- **Name**: create_branch  
- **Description**: Creates a new branch in the repository associated with the current git data source. Uses official Python libraries to create the branch and set it as the current active branch.  
- **User Instructions**:  
  1. Git Server URL  
  2. Git Server authentication token  
- **Usage Note**: Use this tool in combination with the "List Branches In Repo" tool when you want the assistant to create a new branch only if it doesn't already exist.

### Create Pull Request Tool
- **Name**: create_pull_request  
- **Label**: Create Pull/Merge request  
- **Description**: Creates a new pull request (GitHub, Bitbucket) or merge request (GitLab) for an active branch in a Git repository associated with the current git data source. Uses official Python libraries to initiate the request.  
- **User Instructions**:  
  1. Git Server URL  
  2. Git Server authentication token

### Create File Tool
- **Name**: create_file  
- **Description**: Creates a new file with specified content in the current active branch of a Git repository associated with the current git data source. Uses official Python libraries to add the file and commit it to the active branch.  
- **User Instructions**:  
  1. Git Server URL  
  2. Git Server authentication token

### Delete File Tool
- **Name**: delete_file  
- **Description**: Deletes a specified file from the current active branch in the repository associated with the current git data source. Uses official Python libraries to remove the file and commit the deletion.  
- **User Instructions**:  
  1. Git Server URL  
  2. Git Server authentication token

### List Branches Tool
- **Name**: list_branches_in_repo  
- **Description**: Lists all branches in a Git repository associated with the current git data source. Uses official Python libraries to fetch a list of all branches in the repository. It will return the name of each branch.  
- **User Instructions**:  
  1. Git Server URL  
  2. Git Server authentication token

### Update File Tool
- **Name**: update_file  
- **Description**: Updates an existing file in the current active branch of the repository associated with the current git data source. Works by providing the Large Language Model (LLM) with the full file content and asking it to generate a new file with intended changes.  
- **User Instructions**:  
  1. Git Server URL  
  2. Git Server authentication token  
- **Usage Note**: This tool is most effective for small files due to context limitations of the LLM. It may work poorly with large files.  

### Update File Diff Tool
- **Name**: update_file_diff  
- **Description**: Updates an existing file in the current active branch of the repository associated with the current git data source. Uses a "diff" edit format, asking the Large Language Model (LLM) to specify file edits as a series of search/replace blocks.  
- **User Instructions**:  
  1. Git Server URL  
  2. Git Server authentication token  
- **Usage Note**: This tool is efficient as the model only needs to return parts of the file which have changes. It usually performs on par with "Update File" for small files and much better for large files.

### Set Active Branch Tool
- **Name**: set_active_branch  
- **Description**: Changes the current active branch in the repository associated with the current git data source. All subsequent operations, such as file manipulation or Pull Request/Merge Request creation, will be executed in the context of this newly set active branch.  
- **User Instructions**:  
  1. Git Server URL  
  2. Git Server authentication token

### Get PR Changes Tool
- **Name**: get_pr_changes  
- **Label**: Get Pull/Merge Request Changes  
- **Description**: Retrieves all changes associated with a specific Pull Request (GitHub, Bitbucket) or Merge Request (GitLab) in the repository linked to the current git data source. Uses official Python libraries to fetch the diff of changes.  
- **User Instructions**:  
  1. Git Server URL  
  2. Git Server authentication token  
- **Usage Note**: This tool is typically used in combination with "Create Pull/Merge Request Change Comment" for conducting code reviews. It provides the necessary context for the AI assistant to analyze changes.

### Create PR Change Comment Tool
- **Name**: create_pr_change_comment  
- **Label**: Create Pull/Merge Request Change Comment  
- **Description**: Adds a comment to a specific line of changed code in a Pull Request (GitHub, Bitbucket) or Merge Request (GitLab) in the repository associated with the current git data source. Uses official Python libraries to post the comment.  
- **User Instructions**:  
  1. Git Server URL  
  2. Git Server authentication token  
- **Usage Note**: Use this tool after "Get Pull/Merge Request Changes" to allow the AI assistant to provide feedback on specific lines of code.