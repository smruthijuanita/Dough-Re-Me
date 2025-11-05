"""
Simple FastAPI server to host index.html locally.

Run with:
    python serve.py

Or with uvicorn:
    uvicorn serve:app --reload --host 127.0.0.1 --port 8000
"""
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="Dough-Re-Me Bakery")

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Mount the static folder if it exists
static_path = os.path.join(BASE_DIR, "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.get("/")
async def serve_index():
    """Serve the index.html file."""
    index_path = os.path.join(BASE_DIR, "index.html")
    return FileResponse(index_path)


if __name__ == "__main__":
    import uvicorn
    print(" Starting Dough-Re-Me Bakery server...")
    print(" Open http://127.0.0.1:8000 in your browser")
    print(" Press CTRL+C to stop")
    uvicorn.run(app, host="127.0.0.1", port=8000)
