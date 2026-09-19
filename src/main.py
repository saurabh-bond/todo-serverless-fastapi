import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from src.api.v1 import todo, auth
from src.config import settings


logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = FastAPI(
    title="Serverless Todo API",
    version="1.0.0",
    root_path=settings.ROOT_PATH or ""
)

# CORS configurations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
# Public Authentication Endpoints
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth Gateways"])

# Protected Business Domain Logic Endpoints
app.include_router(todo.router, prefix="/api/v1/todos", tags=["Protected Todo Workflows"])


@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}


# Mangum Handler that AWS Lambda targets
handler = Mangum(app, lifespan="off")