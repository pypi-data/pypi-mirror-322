# Notification Toolkit Description

The `NotificationToolkit` class provides an interface for managing notification tools, specifically email and Telegram. It inherits from `BaseToolkit` and includes configurations for both tools.

## Key Classes:

### NotificationToolkitUI
- Represents the User Interface for the Notification Toolkit.
- Contains metadata for tools, including Email and Telegram tools.

### NotificationToolkit
- Inherits from `BaseToolkit`.
- Contains optional configurations for email and Telegram.

## Methods:

### get_tools_ui_info
- Returns UI information for notification tools.

### get_tools
- Returns a list of initialized tools (Email and Telegram).

### get_toolkit
- Initializes the toolkit with provided email and Telegram configurations.

### email_integration_healthcheck
- Checks the health of the email integration and returns the status.