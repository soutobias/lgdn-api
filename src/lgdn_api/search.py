import json
from lgdn_api.db import DuckDBService

con = DuckDBService().conn


def search_by_point(lon: float, lat: float, k: int = 5) -> list[dict]:
    """Search for similar embeddings based on a given longitude and latitude."""
    query = """
        WITH search_embedding AS (
            SELECT chips_id AS search_chip_id, vec
            FROM embeddings
            WHERE ST_Contains(geom, ST_Point(?, ?))
            LIMIT 1
        )
        SELECT
            e.chips_id,
            array_cosine_similarity(e.vec, se.vec) AS similarity,
            ST_AsGeoJSON(e.geom) AS geom_geojson
        FROM embeddings e
        CROSS JOIN search_embedding se
        WHERE e.chips_id != se.search_chip_id
        ORDER BY similarity DESC
        LIMIT ?;
    """

    rows = con.execute(query, [lon, lat, k]).fetchall()

    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": json.loads(r[2]),
                "properties": {
                    "chips_id": r[0],
                    "similarity": float(r[1]),
                    "thumbnail_url": (f"https://lgnd-fullstack-takehome-thumbnails.s3.us-east-2.amazonaws.com/{r[0]}_256.jpeg"),
                    "thumbnail_native": (f"https://lgnd-fullstack-takehome-thumbnails.s3.us-east-2.amazonaws.com/{r[0]}_native.jpeg"),
                },
            }
            for r in rows
        ],
    }
