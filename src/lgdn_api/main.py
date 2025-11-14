import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mcp import FastApiMCP
from lgdn_api.routers import search

app = FastAPI(title="LGDN REST API", version="0.1.0", openapi_url="/openapi.json", docs_url="/docs")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST", "HEAD", "OPTIONS", "PUT", "DELETE"],
    allow_headers=["Access-Control-Allow-Headers", "Content-Type", "Authorization", "Access-Control-Allow-Origin"],
    allow_credentials=True,
)

app.include_router(search.router)


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint to verify if the server is running."""
    return {"status": "healthy"}


mcp = FastApiMCP(app)
mcp.mount_http()
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104
