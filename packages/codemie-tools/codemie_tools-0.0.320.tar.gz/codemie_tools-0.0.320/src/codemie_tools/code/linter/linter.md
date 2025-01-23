# Business Description for Linter Class

## Overview
The `Linter` class is an abstract base class designed for implementing code linters. It provides a structure for linting code changes by defining a standardized interface that must be implemented by any specific linter class. The primary goal is to ensure code quality and adherence to coding standards by analyzing differences between the original and modified code.

## Key Features
- **Abstract Method**: The `lint_code_diff` method must be implemented in derived classes to provide specific linting logic for comparing the old and new content of the code.
- **Changed Lines Detection**: The `get_changed_lines` static method identifies lines that have changed between the old and new code content, facilitating focused linting on the modified sections of the code.

## Methods
- `lint_code_diff(old_content: str, new_content: str) -> Tuple[bool, str]`
  - This abstract method takes two strings representing the original and new code content and returns a tuple. The first element is a boolean indicating whether the linting passed, and the second is a string that contains the linting results or any error messages.

- `get_changed_lines(old_content: str, new_content: str) -> Dict[int, str]`
  - This static method calculates and returns a dictionary of changed lines, where the key is the line number and the value is the new line content. It helps in pinpointing exactly what changes have been made, which can be particularly useful for the linting process.