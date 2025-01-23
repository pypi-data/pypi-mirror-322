# Sonar Tool Documentation

## Overview
The Sonar tool interacts with the SonarQube REST API to retrieve data related to code quality and issues.

## Tool Metadata
- **Name:** Sonar
- **Label:** Sonar

## Description
The SonarQube Tool for interacting with the SonarQube REST API requires specific parameters to function:

### Required Parameters:
1. **relative_url**: This parameter specifies the relative URI for the SONAR REST API.
   - The URI must start with a forward slash, such as `/api/issues/search..`.
   - **Note:** Do not include query parameters in the URL; they should be included in the 'params'.

### Optional Parameters:
2. **params**: This is an optional JSON string containing parameters to be sent in query params. It must be a valid JSON string. For search/read operations, include the following fields:
   - **cleanCodeAttributeCategories**: (consistent, intentional, adaptable, responsible)
   - **severities**: (MINOR, MAJOR, INFO, etc.)
   - **issueStatuses**: (OPEN, ACCEPTED, FIXED, etc.)
   - **types**: (CODE_SMELL, VULNERABILITY, BUG)
   - **ps**: (page size, to set maxResults)

### Defaults and Clarifications:
If any required information is not provided by the user, the tool will attempt to use default values or prompt the user for clarification.

## User Description
The purpose of the Sonar tool is to retrieve data using the SonarQube API. Before using it, the following integrations must be added:
1. SonarQube Server URL
2. SonarQube user token for authentication
3. Project name of the desired repository

### Example User Query:
"Show me the first 10 open major code smells"
