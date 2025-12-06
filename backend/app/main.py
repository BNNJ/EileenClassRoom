"""FastAPI application initialization."""

from fastapi import FastAPI

from app.api.health import router as health_router

# from fastapi.middleware.cors import CORSMiddleware

# from app.config import settings

app = FastAPI(
    title="EileenClassRoom API",
    description="Class management API for preschool parents",
    version="0.1.0",
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
