# LinterFacade Class

## Overview
The `LinterFacade` class acts as a facade for different linters, providing a simplified interface for linting code in various programming languages. Currently, it supports Python linting through the `PythonLinter` implementation.

## Components
- **PYTHON_LINTER_ERROR_CODES**: A string that defines specific error codes for Python linting. Defaults to `"E999,F821"`.
- **linters**: A dictionary that maps language names to their respective linter instances. Currently, it includes only the Python linter.

## Methods
### `__init__`
Initializes the `LinterFacade` instance and sets up the available linters.

### `lint_code(lang: str, old_content: str, content_candidate: str) -> Tuple[bool, str]`
- **Parameters**:
  - `lang`: A string representing the programming language of the content.
  - `old_content`: The original code content before changes.
  - `content_candidate`: The modified code content to be linted.
- **Returns**: A tuple containing a boolean indicating success and a string with any linting messages.
- **Behavior**: Looks up the appropriate linter based on the language provided. If the language is unsupported, it logs an info message and returns success with an empty message. If a valid linter is found, it delegates the linting process to the linter's `lint_code_diff` method.