# Git Utilities Module

This module provides utility functions for managing Git credentials and initializing API wrappers for various Git services (GitLab, GitHub, Bitbucket). It leverages the Pydantic library for data validation and logging for error handling.

## Class: GitCredentials

### Attributes:
- `token`: str - The access token used for authentication.
- `token_name`: Optional[str] - An optional name for the token.
- `repo_link`: str - The link to the Git repository.
- `base_branch`: str - The base branch for the repository.

## Functions:

### 1. `init_gitlab_api_wrapper(git_creds: GitCredentials) -> Optional[CustomGitLabAPIWrapper]`
Initializes and returns a GitLab API wrapper object using the provided credentials.

### 2. `init_github_api_wrapper(git_creds: GitCredentials)`
Initializes and returns a GitHub API wrapper object using the provided credentials.

### 3. `init_bitbucket_api_wrapper(git_creds: GitCredentials)`
Initializes and returns a Bitbucket API wrapper object using the provided credentials.

### 4. `validate_gitlab_wrapper(api_wrapper: [CustomGitLabAPIWrapper], git_creds: GitCredentials)`
Validates the GitLab API wrapper and raises an error if the credentials are invalid.

### 5. `validate_bitbucket(bitbucket: Optional[Repository], git_creds: GitCredentials)`
Validates the Bitbucket API wrapper and raises an error if the credentials are invalid.

### 6. `validate_github_wrapper(api_wrapper: Optional[CustomGitHubAPIWrapper], git_creds: GitCredentials)`
Validates the GitHub API wrapper and raises an error if the credentials are invalid.

### 7. `split_git_url(git_url: str) -> Tuple[str, str]`
Splits a Git URL into its base URL and repository path.

## Error Handling
The module utilizes logging to track errors during API wrapper initialization and credential validation, improving maintainability and debugging capabilities.