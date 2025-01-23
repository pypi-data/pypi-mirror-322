# Tools Variables Documentation

## GitHub Tool

### Name
**github**

### Description
Tool implemented with python rest client and is used to work with Github Public REST API. Accepts a single JSON object which MUST contain: 'method', 'url', 'method_arguments', 'header' that will later be passed to the python requests library. The authorization token will be passed as a header parameter. All parameters MUST be generated based on the Github Public REST API specification. The request MUST be a valid JSON object that will pass json.loads validation. The URL MUST be a valid HTTPS URL and start with `https://api.github.com`.

### User Description
Provides access to the GitHub REST API, allowing for a wider range of operations compared to tools using official Python libraries. This tool enables the AI assistant to perform various GitHub-specific tasks and retrieve detailed information about repositories, issues, pull requests, and more. Before using it, it is necessary to add a new integration for the tool by providing:
1. GitHub Server URL
2. GitHub Personal Access Token with appropriate scopes

### Usage Note
Use this tool when you need to perform GitHub-specific operations that are not covered by other specialized tools.

---

## GitLab Tool

### Name
**gitlab**

### Description
Tool implemented with python rest client and is used to work with Gitlab Public REST API. Accepts a single JSON object which MUST contain: 'method', 'url', 'method_arguments', 'header' that will later be passed to the python requests library. The authorization token will be passed as a header parameter. All parameters MUST be generated based on the Gitlab Public REST API specification. The request MUST be a valid JSON object that will pass json.loads validation. The URL MUST always start with `/api/v4/`.

### User Description
Provides access to the Gitlab REST API, allowing for a wider range of operations compared to tools using official Python libraries. This tool enables the AI assistant to perform various Gitlab-specific tasks and retrieve detailed information about repositories, issues, pull requests, and more. Before using it, it is necessary to add a new integration for the tool by providing:
1. Gitlab Server URL
2. Gitlab Personal Access Token with appropriate scopes

### Usage Note
Use this tool when you need to perform Gitlab-specific operations that are not covered by other specialized tools.