from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging

from src.config import Config

logger = logging.getLogger("uvicorn.access")
logger.disabled = True

domain = Config.BACKEND_DOMAIN

def register_middleware(app: FastAPI):
    # Custom logging middleware
    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)
        processing_time = round(time.time() - start_time, 4)

        print(
            f"{request.client.host}:{request.client.port} - {request.method} {request.url.path} "
            f"-> {response.status_code} in {processing_time}s"
        )
        return response

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "https://udyam-demo.vercel.app",
            f"https://{domain}"
        ],
        allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, PUT, DELETE, etc.)
        allow_headers=["*"],  # Allow all headers (safer for development)
        allow_credentials=True,
    )

    # Trusted hosts
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[
            domain,            
            "localhost",
            "127.0.0.1",
            "0.0.0.0",
            "testserver",
            "udyam-demo.vercel.app"
        ],
    )
