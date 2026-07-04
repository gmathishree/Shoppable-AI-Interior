"""
Shoppable AI Interior Designer - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from routers import vision, generate, shopping, projects, health

app = FastAPI(
    title="Shoppable AI Interior Designer",
    description="AI-powered interior design with interactive e-commerce integration",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(vision.router, prefix="/api/vision", tags=["Vision Analysis"])
app.include_router(generate.router, prefix="/api/generate", tags=["Generation"])
app.include_router(shopping.router, prefix="/api/shopping", tags=["Shopping"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])

# Serve uploads directory
os.makedirs("uploads", exist_ok=True)
os.makedirs("generated", exist_ok=True)
os.makedirs("crops", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/generated", StaticFiles(directory="generated"), name="generated")
app.mount("/crops", StaticFiles(directory="crops"), name="crops")

@app.get("/")
async def root():
    return {"message": "Shoppable AI Interior Designer API", "version": "1.0.0", "status": "running"}
