# **LGDN REST API**


The **LGDN REST API** provides endpoints for similarity search using geospatial embeddings, OpenStreetMap (OSM) semantic search, and real-time weather retrieval.
It also exposes the API through the **Model Context Protocol (MCP)** for tool-based interaction (e.g., ChatGPT Tools, AI agents, or other machine-driven environments).

This document explains:

* The MCP integration
* REST API endpoints
* Database/Data Architecture
* OSM search logic
* Weather service
* Backend components


## Installation

Install dependencies using Poetry:

```bash
pip install poetry
poetry install
```

Download the DuckDB database file (`embeddings.db`) and place it in the project root.

```bash
aws s3 cp --no-sign-request s3://lgnd-fullstack-takehome/embeddings.db .
```

## Usage

```bash
uvicorn lgdn_api.main:app --host 0.0.0.0 --port 8000
```

And access the Swagger UI at: [http://localhost:8000/docs](http://localhost:8000/docs)

## Features

### **1. MCP Integration**

The API uses **FastApiMCP** to expose the service according to the **Model Context Protocol**, enabling tools and agents to call API endpoints programmatically.

The MCP provides a standardized way for LLMs and AI agents to interact with external services via defined tools. Once mounted:

* All FastAPI routes become available as MCP actions.
* Tool metadata is generated automatically from the OpenAPI schema.
* MCP clients can call functions such as:

  * `search_by_point`
  * `search_by_osm_query`
  * `get_weather`

### **2. Search Endpoints**

These endpoints perform spatial and semantic search using DuckDB with spatial extensions and pre-computed embeddings.

**2.1 Search by Geographic Point**

**POST** `/search/point`
**operation_id:** `search_by_point`

Search for similar embedding vectors near a longitude/latitude.

**Body**:

```json
{
  "lon": -122.42,
  "lat": 37.77,
  "k": 5
}
```

**Response**:


```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": { ... },
      "properties": {
        "chips_id": "1234",
        "similarity": 0.94,
        "thumbnail_url": "...256.jpeg",
        "thumbnail_native": "...native.jpeg"
      }
    }
  ]
}
```

**2.2 Search by OSM Query**

**POST** `/search/osm_query`
**operation_id:** `search_by_osm_query`

Searches OSM for a semantic feature (e.g., *marina*, *airport*, *parking*) and then performs an embedding similarity search at that location.

**Request Body**

```json
{
  "query": "marina",
  "limit": 5
}
```

**Response**

Same format as `/search/point`.


**2.3 Weather**

**POST** `/search/weather`
**operation_id:** `get_weather`

Fetches live weather data using **Open-Meteo**.

**Body**

```json
{
  "lon": -122.42,
  "lat": 37.77
}
```

**Response**

```json
{
  "temperature_2m": 59.4,
  "relative_humidity_2m": 62,
  "wind_speed_10m": 4.0,
  ...
}
```
