# CodeExecutor Class

## Overview
The `CodeExecutor` class abstracts communication with code interpreters and runtimes, primarily supporting the execution of Python code. There is potential for expanding support to other programming languages in the future.

## Key Features
- **Language Support**: Currently supports executing Python code.
- **Asynchronous Execution**: Utilizes asynchronous programming for executing code snippets in a sandboxed environment.
- **Custom Exception Handling**: Implements a custom exception class for unsupported languages.

## Class Details
### CodeExecutor
- **Initialization**: Requires a `file_repository` to manage file storage.
- **Methods**:
  - `execute_python(code: str, user_id: str)`: Executes a given Python code snippet.
  - `_execute_code(code: str, user_id: str, language)`: Executes the provided code snippet in the specified programming language.
  - `_run_in_sandbox(code: str, user_id: str)`: Runs the code in a secure sandbox environment provided by `CodemieBox`.

### UnsupportedLanguageException
- Custom exception raised when an unsupported programming language is attempted to be executed.

### CodemieBox
- Inherits from `LocalBox` and manages the temporary directory for code execution.
- Responsible for starting and stopping a Jupyter kernel gateway to execute the code.