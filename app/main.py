"""Main FastAPI application with PostgreSQL database."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

from app.core.config import settings
from app.api.v1 import products, orders

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Bakery API with PostgreSQL database"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(products.router, prefix="/api/v1/products", tags=["products"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["orders"])

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Mount static files
static_path = os.path.join(BASE_DIR, "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.get("/")
async def serve_index():
    """Serve the index.html file."""
    index_path = os.path.join(BASE_DIR, "index.html")
    return FileResponse(index_path)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "database": "postgresql"}


if __name__ == "__main__":
    import uvicorn
    print("🥖 Starting Dough-Re-Me Bakery server with PostgreSQL...")
    print("📍 Frontend: http://127.0.0.1:8000")
    print("📍 API Docs: http://127.0.0.1:8000/docs")
    print("⏹️  Press CTRL+C to stop")
    uvicorn.run(app, host="127.0.0.1", port=8000)
