# CSVTool Class

## Overview
The `CSVTool` class is a specialized tool for working with data from CSV files. It is designed to simplify data manipulation using the Pandas library.

## Inheritance
The `CSVTool` class inherits from `CodeMieTool`, which provides a base functionality for all tools in the CodeMie platform.

## Attributes
- **args_schema**: Defines the input schema for the tool using Pydantic's `BaseModel`.
- **name**: The name of the tool as defined in `CSV_TOOL`.
- **label**: The label of the tool as defined in `CSV_TOOL`.
- **description**: A description of the tool as defined in `CSV_TOOL`.
- **csv_content**: Holds the content of the CSV file, which is excluded from the model schema.
- **_length_to_sniif**: A constant that defines the number of bytes to sniff for detecting the CSV delimiter.

## Input Class
### Input
The `Input` class is a Pydantic model that defines the input parameters required for executing methods on the Pandas DataFrame:
- **method_name**: The name of the method to be called on the DataFrame.
- **method_args**: A dictionary of arguments to be passed to the method.
- **column**: Optional; specifies the column to be used for the operation.

## Methods
### execute(method_name: str, method_args: dict = {}, column: Optional[str] = None)
Executes the specified method on the DataFrame or a specific column.

### bytes_content() -> bytes
Returns the content of the file as bytes. Raises a `ValueError` if the content is not set.

### _get_csv_delimiter(data: str) -> str
Determines the delimiter used in the CSV file by sniffing the first few bytes of the data.

## Usage
To use the `CSVTool`, create an instance with the CSV content and call the `execute` method with the appropriate parameters.