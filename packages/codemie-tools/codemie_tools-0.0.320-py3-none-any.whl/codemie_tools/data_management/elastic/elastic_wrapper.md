# Elastic Wrapper Documentation

## Overview
The `elastic_wrapper.py` file contains a class `SearchElasticIndexResults` that serves as a wrapper for interacting with Elasticsearch indices. It provides methods to create a client and perform search operations on the specified indices.

## Dependencies
- `elasticsearch`: This package is required to interact with Elasticsearch. If it's not installed, an ImportError is raised.

## Classes
### SearchElasticIndexResults
This class includes methods for managing the connection to Elasticsearch and executing search queries.

#### Methods
1. **_get_client(elastic_config: ElasticConfig) -> Optional[Elasticsearch]**  
   This class method initializes the Elasticsearch client using the provided configuration. It checks if the necessary package is installed and retrieves the client based on the presence of an API key.

   - **Parameters:**
     - `elastic_config`: An instance of `ElasticConfig` that contains the configuration for the Elasticsearch connection.
   - **Returns:**
     - An instance of `Elasticsearch` if successful; otherwise, raises an ImportError.

2. **search(index: str, query: str, elastic_config: ElasticConfig)**  
   This class method executes a search query on the specified index using the provided configuration.

   - **Parameters:**
     - `index`: The name of the index to search.
     - `query`: The search query in the body format.
     - `elastic_config`: An instance of `ElasticConfig` for connection parameters.
   - **Returns:**
     - The search results from Elasticsearch.