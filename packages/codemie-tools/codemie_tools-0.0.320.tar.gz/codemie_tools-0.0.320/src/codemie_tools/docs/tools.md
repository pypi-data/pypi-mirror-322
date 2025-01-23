# Research Tools in CodeMie

## Overview
The `tools.py` file located in the `src/codemie_tools/research/` directory provides various tools for web scraping and data retrieval from different sources, including Google Search and Wikipedia. This module is part of the CodeMie platform, aiming to empower users with research capabilities through automated tools.

## Key Components

### 1. WebScrapperTool
- **Description**: A tool designed to scrape information from web pages.
- **Functionality**: Uses the BeautifulSoup library to parse HTML and extract raw text content from a specified URL.
- **Usage**: Ideal for gathering unstructured data from online resources.

### 2. GoogleSearchResults
- **Description**: A tool that allows users to perform Google searches and retrieve results.
- **Functionality**: Utilizes the GoogleSearchAPIWrapper to execute search queries and return the results in a structured format.
- **Usage**: Useful for obtaining specific information or data points from Google search results.

### 3. GooglePlacesTool
- **Description**: A tool for interacting with Google Places API to retrieve location-based information.
- **Functionality**: Allows users to query places (locations) based on specific criteria.
- **Usage**: Helpful for applications requiring geographical information, such as local businesses or points of interest.

### 4. GooglePlacesFindNearTool
- **Description**: A specialized tool to find places near a specified location.
- **Functionality**: Takes the current location and a target query to search for nearby locations. Users can also specify a search radius.
- **Usage**: Ideal for applications needing to suggest nearby services or locations based on user input.

### 5. WikipediaQueryRun
- **Description**: A tool for querying Wikipedia.
- **Functionality**: Uses the WikipediaAPIWrapper to execute queries and fetch relevant information from Wikipedia.
- **Usage**: Great for obtaining information or summaries from Wikipedia articles directly.

## Potential Business Value
By employing these research tools, organizations can significantly enhance their data collection and analysis capabilities. The ability to automate the gathering of information from various sources reduces manual effort, increases efficiency, and allows for more comprehensive research. This can lead to better decision-making, improved customer insights, and the development of data-driven strategies in various business domains.