# Image Tool

## Description
The `ImageTool` class is designed to interact with the GPT-Vision model to analyze and transcribe the contents of images. This tool is part of the CodeMie framework and is implemented in the `src/codemie_tools/vision/image_tool.py` file.

## Features
- **Image Analysis**: The tool analyzes images and provides a detailed description of their contents.
- **Text Transcription**: If an image contains text, the tool transcribes that text.

## Components
- **Input Model**: Defined using Pydantic's `BaseModel`, the `Input` class takes a detailed user query for image recognition.
- **Execution**: The `execute` method checks if the image content is set and then calls the `generate` method to produce the analysis and transcription.
- **Generate Method**: This method uses the `chat_model` to invoke a conversation with the GPT-Vision model, sending the image and the prompt for analysis.
- **Base64 Conversion**: The `base64_content` method converts the image content into a base64 string format suitable for web usage.

## Usage
To use the `ImageTool`, instantiate the class, set the image content, and call the `execute` method with the appropriate query. The output will include the analysis and any transcribed text from the image.