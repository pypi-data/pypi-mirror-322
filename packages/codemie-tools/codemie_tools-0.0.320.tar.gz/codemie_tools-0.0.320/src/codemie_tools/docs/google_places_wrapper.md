# Google Places API Wrapper

## Overview
The `GooglePlacesAPIWrapper` class is designed to interact with the Google Places API. It allows users to search for places based on queries, find nearby places, and fetch detailed information about specific places. 

## Features
- **Search for Places**: The `places` method allows users to search for places matching a specific query.
- **Find Nearby Places**: The `find_near` method lets users find places near a specified location within a defined radius.
- **Fetch Place Details**: The `fetch_place_details` method retrieves detailed information about a place, including its name, address, phone number, and website.

## Configuration
- **API Key**: Users need to provide a Google Places API key either through the environment variable `GPLACES_API_KEY` or directly in the class instantiation.

## Usage Example
```python
# Initialize the wrapper
wrapper = GooglePlacesAPIWrapper(gplaces_api_key="YOUR_API_KEY")

# Search for places
results = wrapper.places("restaurants in New York")
print(results)

# Find nearby places
nearby_places = wrapper.find_near("Times Square, New York", "restaurant", radius=1000)
print(nearby_places)
```

## Potential Value
The `GooglePlacesAPIWrapper` class can significantly enhance applications that require geographic data by providing easy access to extensive information about places. This can be useful for:
- Location-based services
- Travel and tourism applications
- Business directory services
- Event planning applications

By integrating this functionality, businesses can improve user experience and engagement through personalized recommendations and streamlined access to location-based information.