# Telegram Tool

## Overview
The `TelegramTool` class is designed to interact with the Telegram Bot API, allowing users to send messages and perform other actions through HTTP requests.

## Classes

### TelegramConfig
This class defines the configuration for the Telegram bot, specifically the bot token required for authentication.

### TelegramToolInput
This class defines the input schema for the tool's execution method. It includes:
- **method**: The HTTP method to use for the request (GET, POST). Required parameter.
- **relative_url**: The relative URL of the Telegram Bot API to call, e.g. 'sendMessage'. Required parameter. For GET method, query parameters should be included in the URL.
- **params**: Optional JSON string of parameters to be sent in the request body or as query parameters. Must include the "chat_id" for sending messages.

### TelegramTool
Inherits from `CodeMieTool`. The main tool for executing requests to the Telegram Bot API. Key methods include:
- **execute(method: str, relative_url: str, params: Optional[str] = '')**: Sends a request to the Telegram API. Raises a ValueError if the Telegram config is not set.
- **parse_payload_params(params: Optional[str]) -> Dict[str, Any]**: Parses the JSON string of parameters into a dictionary.

## Usage
To use the `TelegramTool`, you need to set the `telegram_config` with the bot token before executing any methods. The tool can perform various actions based on the provided method and URL.