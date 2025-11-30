"""
Entry point for running the FastAPI application.
Run with: uv run python main.py
Or: uv run uvicorn app.main:app --reload --port 3000
"""
from app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000, reload=True)
