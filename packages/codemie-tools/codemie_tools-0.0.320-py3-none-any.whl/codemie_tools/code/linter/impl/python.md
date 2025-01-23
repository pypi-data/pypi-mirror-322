# PythonLinter Class

The `PythonLinter` class is a specific implementation of a linter for Python code, inheriting from the base `Linter` class. It provides functionalities to lint Python code, particularly focusing on the differences between old and new versions of the code.

## Attributes
- **error_codes**: A string representing the specific error codes to be checked by the linter.

## Methods

### `__init__(self, error_codes)`
Initializes the `PythonLinter` with the specified error codes.

### `lint_code_diff(self, old_content: str, new_content: str) -> Tuple[bool, str]`
Lints the differences between the old and new code content. Returns a tuple indicating whether there are errors and an error message if applicable.

### `lint_single_code(self, content: str) -> Dict[int, str]`
Lints a single piece of code and returns a dictionary of errors found, mapped by line number.

### `_run_flake8_cli(content: str, error_codes: str)`
Runs the `flake8` command-line interface on the provided content and returns the output errors.

### `_filter_new_errors(errors: Dict[int, str], changed_lines: Dict[int, str]) -> List[Tuple[str, str]]`
Filters the errors to retain only those that correspond to the lines that have changed.

### `_format_errors(errors: List[Tuple[str, str]]) -> str`
Formats the errors for display, showing the line content and the corresponding error message.