"""
Bug2PR FastAPI Application
Main entry point with CORS, health check, and custom OpenAPI schema
"""

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from typing import Optional
import logging

from app.config import settings
from app.database import db

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Autonomous bug-to-PR pipeline with AI agents",
    debug=settings.debug
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_openapi():
    """
    Custom OpenAPI schema to handle Pydantic 2.13+ ForwardRef issue with UploadFile
    This prevents the 'PydanticUndefined' error in OpenAPI schema generation
    """
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Fix UploadFile schema if it exists
    if "components" in openapi_schema and "schemas" in openapi_schema["components"]:
        schemas = openapi_schema["components"]["schemas"]
        
        # Handle UploadFile schema
        if "Body_upload_file" in schemas:
            upload_schema = schemas["Body_upload_file"]
            if "properties" in upload_schema:
                for prop_name, prop_schema in upload_schema["properties"].items():
                    if isinstance(prop_schema, dict) and prop_schema.get("type") == "string" and prop_schema.get("format") == "binary":
                        # Ensure proper binary file schema
                        prop_schema["type"] = "string"
                        prop_schema["format"] = "binary"
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Override the default OpenAPI schema
app.openapi = custom_openapi


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Database initialized at {settings.database_url}")
    logger.info(f"CORS enabled for origins: {settings.cors_origins_list}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info(f"Shutting down {settings.app_name}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    Returns application status and configuration info
    """
    try:
        # Test database connection
        projects_count = len(db.list_projects())
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "healthy",
                "app_name": settings.app_name,
                "version": settings.app_version,
                "database": "connected",
                "projects_count": projects_count,
                "ollama_url": settings.ollama_base_url,
                "github_configured": bool(settings.github_token),
                "google_ai_configured": bool(settings.google_api_key),
                "groq_configured": bool(settings.groq_api_key)
            }
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )


@app.get("/api/config")
async def get_config():
    """Get public configuration (non-sensitive)"""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "ollama_model": settings.ollama_model,
        "google_model": settings.google_model,
        "groq_model": settings.groq_model,
        "max_iterations": settings.max_iterations,
        "agent_timeout": settings.agent_timeout
    }


# Import and include routers (will be created later)
# from app.routes import projects, risks, agents
# app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
# app.include_router(risks.router, prefix="/api/risks", tags=["risks"])
# app.include_router(agents.router, prefix="/api/agents", tags=["agents"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )

# Made with Bob
