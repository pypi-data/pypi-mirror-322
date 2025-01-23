# Data Management Toolkit

## Overview
The `DataManagementToolkit` class is a part of the `codemie_tools` library, designed to manage various data management tasks using both ElasticSearch and SQL tools.

## Features
- **ElasticSearch Integration**: Provides functionality to interact with ElasticSearch indices.
- **SQL Database Management**: Offers tools for managing SQL databases.

## Class Structure
### DataManagementToolkit Class
- Inherits from: `BaseToolkit`
- **Attributes**:
  - `elastic_config`: Optional configuration for ElasticSearch.
  - `sql_config`: Optional configuration for SQL databases.

### Methods
- **get_tools_ui_info**: Returns user interface information for the tools available in the toolkit.
- **get_tools**: Instantiates and returns the tools available (SQL and ElasticSearch).
- **get_toolkit**: A class method that constructs the `DataManagementToolkit` with the provided configurations for ElasticSearch and SQL.

## Usage
You can create an instance of the `DataManagementToolkit` by providing the necessary configurations for ElasticSearch and SQL databases. This toolkit can then be used to access various tools for data management tasks.