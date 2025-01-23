# SQL Models Description

## Overview
This module defines the data models used for managing SQL configurations in the application. It utilizes Pydantic for data validation and type enforcement.

## Components

### SQLDialect Enum
The `SQLDialect` enumeration defines the supported SQL dialects:
- `MYSQL`: Represents the MySQL database.
- `POSTGRES`: Represents the PostgreSQL database.

### SQLConfig Class
The `SQLConfig` class is a Pydantic model that holds the configuration for connecting to an SQL database. It includes the following fields:
- `dialect`: The type of SQL database (e.g., mysql, postgres).
- `host`: The hostname of the database server.
- `port`: The port number on which the database server is listening.
- `username`: The username for authenticating with the database.
- `password`: The password for authenticating with the database.
- `database_name`: The name of the database to connect to.

#### Validation
The `validate_config` class method ensures that all required fields are provided before creating an instance of `SQLConfig`. If any field is missing, a `ValueError` is raised, indicating which field is required.