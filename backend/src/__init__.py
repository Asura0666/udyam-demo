from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.routes.aadhaar_routes import aadhaar_router
from src.routes.pan_routes import pan_router
from src.routes.udyam_routes import udyam_router
from src.middleware import register_middleware

version = "v1"

description = """
  Udyam-backend by Asura
"""

version_prefix = f"/api/{version}"

app = FastAPI(
    title="Udyam-Backend",
    description=description,
    version=version,
    license_info={"name": "MIT License", "url": "https://opensource.org/license/mit"},
    contact={
        "name": "Dhiraj Lande",
        "url": "https://github.com/asura0666",
        "email": "landedhiraj928@gmail.com",
    },
    terms_of_service="httpS://example.com/tos",
    openapi_url=f"{version_prefix}/openapi.json",
    docs_url=f"{version_prefix}/docs",
    redoc_url=f"{version_prefix}/redoc",
)

register_middleware(app)

app.include_router(aadhaar_router, prefix=f"{version_prefix}/aadhaar", tags=["Udyam Aadhaar Verification"])
app.include_router(pan_router, prefix=f"{version_prefix}/pan", tags=["Udyam PAN Verification"])
app.include_router(udyam_router, prefix=f"{version_prefix}/udyam", tags=["Udyam Registration"])


@app.get("/", tags=["Health"])
def health_check():
    return JSONResponse(content={"status": "ok"})
