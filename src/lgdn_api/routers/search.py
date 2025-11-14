from fastapi import APIRouter
from pydantic import BaseModel
from lgdn_api.osm import search_osm_points
from lgdn_api.search import search_by_point
from lgdn_api.weather import get_weather_data

router = APIRouter()


class PointSearchRequest(BaseModel):
    """Request model for point-based search."""

    lon: float
    lat: float
    k: int = 5


class OSMQueryRequest(BaseModel):
    """Request model for OSM query-based search."""

    query: str
    limit: int = 5


class WeatherRequest(BaseModel):
    """Request model for weather data based on longitude and latitude."""

    lon: float
    lat: float


@router.post("/search/point", operation_id="search_by_point")
def search_point(req: PointSearchRequest) -> dict:
    """Search for similar embeddings based on a given longitude and latitude."""
    return search_by_point(req.lon, req.lat, req.k)


@router.post("/search/osm_query", operation_id="search_by_osm_query")
def search_by_osm_query(req: OSMQueryRequest) -> dict:
    """Search for similar embeddings based on a given OSM query (e.g., "marina", "airport")."""
    points = search_osm_points(req.query)
    lon, lat = points[0]

    return search_by_point(lon, lat, req.limit)


@router.post("/search/weather", operation_id="get_weather")
async def get_weather(req: WeatherRequest) -> dict:
    """Get current weather conditions for a given latitude and longitude.

    Uses Open-Meteo API (free, no API key required).
    """
    return get_weather_data(req.lon, req.lat)
