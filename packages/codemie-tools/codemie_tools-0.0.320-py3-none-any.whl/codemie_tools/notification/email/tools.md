# Email Tool

## Overview
The `EmailTool` class is designed for sending emails using the SMTP protocol. It utilizes the `smtplib` library to establish a connection with an SMTP server and send emails to specified recipients.

## Classes
### EmailToolInput
- **recipient_emails**: A list of recipient email addresses.
- **subject**: The subject of the email.
- **body**: The body content of the email.

### EmailTool
- **name**: The name of the email tool.
- **email_creds**: Configuration details for the SMTP server, which are optional.
- **args_schema**: Defines the input schema for the tool using `EmailToolInput`.
- **description**: A description of the email tool.

## Methods
### execute(recipient_emails: str, subject: str, body: str) -> str
This method sends an email to the specified recipient addresses with the provided subject and body content. If email credentials are not provided, it raises a `ValueError`. On success, it returns a success message; otherwise, it returns an error message.

### integration_healthcheck() -> Tuple[bool, str]
This method checks the health of the email integration by trying to connect to the SMTP server with the provided credentials. It returns a tuple containing a boolean indicating success or failure and a corresponding message.