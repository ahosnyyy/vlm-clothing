from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.analyze import router as analyze_router
from app.core.settings import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
    allow_credentials=True,
)

app.include_router(analyze_router, prefix="/analyze-clothing")