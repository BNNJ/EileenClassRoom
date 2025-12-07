"""FastAPI application initialization."""

import os
from fastapi import FastAPI

from app.api.health import router as health_router

# from fastapi.middleware.cors import CORSMiddleware

# from app.config import settings

app = FastAPI(
    title="EileenClassRoom API",
    description="Class management API for preschool parents",
    version=os.getenv("API_VERSION", "dev"),
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)


# Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[settings.FRONTEND_URL, "http://localhost:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


app.include_router(health_router)
