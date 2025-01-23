# Business Description for `utils.py`

The `utils.py` module provides utility functions that aid in handling various common operations within the codebase, particularly focusing on data sanitization and parsing. The following key functionalities are defined in this module:

## Main Functions

### 1. `sanitize_string(input_string: str) -> str`

Sanitizes a string by replacing or masking potentially sensitive information. This includes:
- Passwords
- Usernames
- IP addresses
- Email addresses
- API keys
- Credit card numbers

**Example Usage:**
```python
original_string = "Error: Unable to connect. Username: admin, Password: secret123, IP: 192.168.1.1"
print(sanitize_string(original_string))
# Output: 'Error: Unable to connect. Username: ***, Password: ***, IP: [IP_ADDRESS]'
```

### 2. `parse_to_dict(input_string)`

Parses a string into a dictionary. This function first attempts to decode a JSON formatted string directly. If it fails, it tries to adjust the string by replacing single quotes with double quotes and escaping existing double quotes before re-attempting the parse.

### 3. `parse_tool_input(args_schema: Type[BaseModel], tool_input: Union[str, Dict])`

Parses input parameters based on a provided schema. This function validates and extracts relevant parameters, ensuring that they conform to the expected structure defined by the schema.

## Error Handling
The module also includes error handling mechanisms to manage exceptions that arise during JSON decoding and input parsing, providing informative logging for debugging and operational transparency.

Overall, the `utils.py` module is essential for maintaining data integrity and ensuring that sensitive information is handled securely across the application.