# Tools Variables Documentation

This document provides an overview of the various tools defined in `src/codemie_tools/research/tools_vars.py`.

## Tools Overview

### Google Search Tool
- **Name**: `google_search_tool_json`
- **Label**: Google Search
- **Description**: A wrapper around Google Search. Useful for when you need to answer questions in real time, google information or browse the internet for additional details. Input should be a search query. Output is a JSON array of the query results.
- **User Description**: A wrapper around Google Search. Useful for when you need to answer questions in real time, google information or browse the internet for additional details.

### Google Places Tool
- **Name**: `google_places`
- **Label**: Google Places
- **Description**: A wrapper around Google Places. Useful for when you need to validate or discover addresses from ambiguous text. Input should be a search query.
- **User Description**: A wrapper around Google Places. Useful for when you need to validate or discover addresses from ambiguous text.

### Google Places Find Near Tool
- **Name**: `google_places_find_near`
- **Label**: Google Places Find Near
- **Description**: A wrapper around Google Places API, especially for finding places near a location. Useful for when you need to validate or discover addresses from ambiguous text. Input schema is the following:
  - current_location_query: detailed user query of current user location or where to start from;
  - target: the target location or query which user wants to find;
  - radius: the radius of the search. This is an optional field.
- **User Description**: A wrapper around Google Places API, especially for finding places near a location. Useful for when you need to validate or discover addresses from ambiguous text.

### Tavily Search Tool
- **Name**: `tavily_search_results_json`
- **Label**: Tavily Search
- **Description**: A web search engine optimized for comprehensive, accurate, and trusted results. Useful for when you need to answer questions about current events. Input should be a search query.
- **User Description**: A web search engine optimized for comprehensive, accurate, and trusted results. Useful for when you need to answer questions about current events.

### Wikipedia Tool
- **Name**: `wikipedia`
- **Label**: Wikipedia
- **Description**: A wrapper around Wikipedia. Useful for when you need to answer general questions about people, places, companies, facts, historical events, or other subjects. Input should be a search query.
- **User Description**: A wrapper around Wikipedia. Useful for when you need to answer general questions about people, places, companies, facts, historical events, or other subjects.

### Web Scraper Tool
- **Name**: `web_scrapper`
- **Label**: Web Scraper
- **Description**: A tool to scrape the web. Use this when you need to scrape a website. Input should be a URL. The output will be the text content of the website.
- **User Description**: Extracts text content from a specified web page. Use this tool when you need to gather information from a website that doesn't offer an API.

### Advanced Web Scraper Tool
- **Name**: `advanced_web_scrapper`
- **Description**: (No description provided.)
