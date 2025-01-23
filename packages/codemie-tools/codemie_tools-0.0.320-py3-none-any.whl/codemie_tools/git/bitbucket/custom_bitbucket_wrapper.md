# Custom Bitbucket Wrapper

## Overview
The `custom_bitbucket_wrapper.py` file provides a Python wrapper for interacting with the Bitbucket API. It extends the functionalities of the Atlassian Bitbucket Cloud SDK to facilitate operations such as creating branches, pull requests, and handling file contents within a repository.

## Key Classes

### Sources
- Inherits from `BitbucketCloudBase`
- Overrides the `request` method to handle URL-encoded requests appropriately.
- Provides methods to create and read files or directories within a Bitbucket repository.

### CustomBranches
- Extends the `Branches` class to implement custom branch creation logic that appends a version number if the branch already exists.

### CustomPullRequest
- Extends the `PullRequest` class to add functionality for commenting on pull requests.

### CustomPullRequests
- Extends the `PullRequests` class to utilize the `CustomPullRequest` for better object handling.

### CustomBitbucketApiWrapper
- The main class that combines all functionalities, allowing users to interact with repositories, branches, and pull requests easily.
- Initializes the connection with Bitbucket and provides access to the `sources`, `branches`, and `pullrequests` properties.

## Usage
This wrapper simplifies the interaction with the Bitbucket API, enabling developers to perform repository operations without dealing with the complexity of the API responses directly.