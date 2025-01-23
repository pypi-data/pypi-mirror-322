# FileSystemToolkit

## Overview
The `FileSystemToolkit` class provides a set of tools for file management operations within a specified root directory. It inherits from `BaseToolkit` and is designed to facilitate various file system operations such as reading, writing, and executing commands.

## Core Components
- **FileSystemToolkitUI**: A user interface for the file system toolkit that presents available tools based on user permissions.
- **FileSystemToolkit**: The main class that contains methods for manipulating files and directories.

## Key Classes and Methods
- **get_tools_ui_info(is_admin: bool)**: Returns the UI information for the toolkit, including available tools based on user roles.
- **get_tools()**: Retrieves a list of tools available in the file system toolkit, including reading, writing, and command line tools.
- **get_toolkit(configs: Dict[str, Any])**: A factory method for creating instances of the `FileSystemToolkit` based on configuration settings.

## Available Tools
The toolkit includes the following tools:
- **ReadFileTool**: For reading files from the file system.
- **WriteFileTool**: For writing files to the file system.
- **ListDirectoryTool**: For listing the contents of a directory.
- **CommandLineTool**: For executing command line commands.
- **DiffUpdateFileTool**: For comparing and updating files.
- **PythonRunCodeTool**: For executing Python code.
- **GenerateImageTool**: For generating images using Azure DALL-E.

## Logging
The toolkit uses Python's built-in logging library to log actions and errors, which can be helpful for debugging and monitoring purposes.