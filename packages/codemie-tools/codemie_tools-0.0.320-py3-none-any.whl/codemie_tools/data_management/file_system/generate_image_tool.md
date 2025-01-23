# Generate Image Tool

## Overview
The `GenerateImageTool` is a part of the CodeMie tools that facilitates the generation of images based on textual descriptions using Azure's DALL-E model.

## Components
1. **AzureDalleAIConfig**: Configuration model for Azure DALL-E API which includes:
   - `api_version`: The version of the API to use.
   - `azure_endpoint`: The endpoint URL for the Azure service.
   - `api_key`: The API key to authenticate the requests.

   **Validation**: Ensures that all required fields are provided before use.

2. **GenerateImagesToolInput**: Input model that specifies the required input for image generation:
   - `image_description`: A detailed description of the image to be generated.

3. **GenerateImageTool**: The main tool class that inherits from `CodeMieTool` and implements the image generation logic:
   - **Attributes**:
     - `name`: The name of the tool.
     - `description`: A brief description of the tool's functionality.
     - `args_schema`: Schema that defines the expected input arguments.
     - `model_id`: The identifier for the DALL-E model to be used (default is Dalle3).
     - `azure_dalle_config`: Configuration object for Azure DALL-E (excluded from the input schema).
   - **Methods**:
     - `execute`: Takes an image description, communicates with the Azure OpenAI service to generate an image, and returns the URL of the generated image.

## Usage
To use the `GenerateImageTool`, instantiate it with the necessary Azure DALL-E configuration and call the `execute` method with a description of the desired image. The method will return the URL of the generated image.