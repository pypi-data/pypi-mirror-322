# SQL Tool Description

## Overview
The `SQLTool` class is designed to execute SQL queries against a specified database. It is part of the `codemie_tools` library for data management and provides a structured way to interact with SQL databases.

## Features
- Execute SQL queries and retrieve results.
- Automatically lists available tables and their columns for easier query formulation.
- Supports connection to various SQL databases including PostgreSQL and MySQL.

## Components
### Classes
- **SQLToolInput**: A Pydantic model that defines the input schema for SQL queries, ensuring that the input meets the expected structure.
- **SQLTool**: Inherits from `CodeMieTool` and contains methods to execute SQL queries, list available tables and columns, and manage database connections.

### Methods
1. **execute(sql_query: str)**: Executes the provided SQL query and returns the results.
2. **execute_sql(engine: Engine, sql_query: str)**: The core method that executes the SQL query using a session from SQLAlchemy.
3. **list_tables_and_columns(engine)**: Returns a dictionary containing the names of tables and their respective columns in the connected database.
4. **create_db_connection()**: Establishes a database connection using the configuration provided.

## Usage
To use the `SQLTool`, an instance must be created with the appropriate SQL configuration, and then the `execute` method can be called with a valid SQL query.

## Error Handling
In case of an error during query execution, the tool provides feedback on the error and suggests checking the available tables and columns.