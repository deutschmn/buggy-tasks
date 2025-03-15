from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__

app = FastAPI(
    title="Buggy AF",
    description="A FastAPI service for machine learning model training and inference",
    version=__version__,
)

# Configure CORS, allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "Buggy AF",
        "version": __version__,
        "description": "Machine Learning API for model training and inference",
    }
