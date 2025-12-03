"""Main FastAPI application with Supabase backend."""
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import logging

from app.core.config import settings
from app.db.supabase import get_client
from app.api.v1 import products, orders
from app.api.v1 import assistant

# Create FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    import logging
    try:
        # Assistant readiness log without importing client
        from app.llm_client import settings as llm_settings
        if llm_settings.groq_api_key:
            logging.info("Assistant client configured (GROQ_API_KEY present).")
        else:
            logging.warning("Assistant client not configured. Set GROQ_API_KEY in .env to enable AI assistant.")
    except Exception as e:
        logging.error(f"Assistant lifespan init failed: {e}")
    # Supabase readiness
    try:
        client = get_client()
        client.table("desserts").select("id").limit(1).execute()
        app.state.supabase_ok = True
        logging.info("Supabase client configured and reachable.")
    except Exception as e:
        app.state.supabase_ok = False
        logging.warning(f"Supabase client not configured or unreachable: {e}")
    yield
    # No teardown logic needed

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Bakery API with PostgreSQL database",
    lifespan=lifespan
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
app.include_router(assistant.router, prefix="/api/v1/assistant", tags=["assistant"])

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Mount static files
static_path = os.path.join(BASE_DIR, "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")


# Removed deprecated @app.on_event, using lifespan above


@app.get("/")
async def serve_index():
    """Serve the index.html file."""
    index_path = os.path.join(BASE_DIR, "index.html")
    return FileResponse(index_path)


@app.get("/cart.html")
async def serve_cart():
    """Serve the cart.html file."""
    cart_path = os.path.join(BASE_DIR, "cart.html")
    return FileResponse(cart_path)


@app.get("/product.html")
async def serve_product():
    """Serve the product.html file."""
    product_path = os.path.join(BASE_DIR, "product.html")
    return FileResponse(product_path)


@app.get("/orders.html")
async def serve_orders():
    """Serve the orders.html file."""
    orders_path = os.path.join(BASE_DIR, "orders.html")
    return FileResponse(orders_path)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    # Assistant status
    try:
        from app.llm_client import settings as llm_settings
        assistant_configured = bool(llm_settings.groq_api_key)
    except Exception:
        assistant_configured = False

    return {
        "status": "healthy",
        "supabase": {"configured": bool(getattr(app.state, "supabase_ok", False))},
        "assistant": {
            "configured": assistant_configured,
            "model": "openai/gpt-oss-20b"
        }
    }


if __name__ == "__main__":
    import uvicorn
    print("🥖 Starting Dough-Re-Me Bakery server (Supabase-backed)...")
    print("📍 Frontend: http://127.0.0.1:8000")
    print("📍 API Docs: http://127.0.0.1:8000/docs")
    print("⏹️  Press CTRL+C to stop")
    uvicorn.run(app, host="127.0.0.1", port=8000)
