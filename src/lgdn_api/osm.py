import requests

# San Francisco Bay Bounding Box
# south,west,north,east
SF_BBOX = "37.3,-122.6,38.1,-121.9"

QUERY_TAGS = {
    "marina": "leisure=marina",
    "marinas": "leisure=marina",
    "harbor": "leisure=marina",
    "airport": "aeroway=aerodrome",
    "airports": "aeroway=aerodrome",
    "airplanes": "aeroway=aerodrome",
    "runway": "aeroway=runway",
    "parking": "amenity=parking",
    "parking lot": "amenity=parking",
    "parking lots": "amenity=parking",
    "stadium": "leisure=stadium",
    "sports": "leisure=stadium",
    "industrial": "landuse=industrial",
    "warehouse": "building=warehouse",
    "solar": "generator:source=solar",
    "solar farm": "generator:source=solar",
    "golf": "leisure=golf_course",
    "golf course": "leisure=golf_course",
}


def search_osm_points(query: str) -> list[tuple[float, float]]:
    """Search OSM for points matching the given query within the SF Bay area."""
    q = query.lower()
    osm_tag = QUERY_TAGS.get(q)
    if not osm_tag:
        return []

    overpass_query = f"""
    [out:json][timeout:25];
    (
        node[{osm_tag}]({SF_BBOX});
        way[{osm_tag}]({SF_BBOX});
        relation[{osm_tag}]({SF_BBOX});
    );
    out center;
    """
    response = requests.post(
        "https://overpass-api.de/api/interpreter",
        data=overpass_query,
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()

    points = []
    for elem in data.get("elements", []):
        center = elem.get("center")
        if center:
            lon, lat = center["lon"], center["lat"]
        else:
            lon, lat = elem.get("lon"), elem.get("lat")

        if lon is not None and lat is not None:
            points.append((lon, lat))

    if not points:
        msg = f"No OSM features found for query: {query}"
        raise RuntimeError(msg)

    return points
