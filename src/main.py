import logging 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from src.api.v1 import todo
from src.config import settings


logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = FastAPI(
    title="Serverless Todo API",
    version="1.0.0",
    root_path=settings.ROOT_PATH # Ensures API Gateway paths match gracefully
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
app.include_router(todo.router, prefix="/app/v1/todos", tags=["Todos"])

@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "healthy", "environment": settings.ENV}

# Mangum Handler that AWS Lambda targets
handler = Mangum(app, lifespan="off")