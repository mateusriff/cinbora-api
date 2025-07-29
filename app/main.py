import uvicorn
from fastapi import FastAPI
from starlette_prometheus import PrometheusMiddleware, metrics
from app.database import create_db_and_tables
from app.routes.address import router as address_router

swagger_ui_parameters = {
    "docExpansion": "none",
    "displayRequestDuration": True,
    "filter": True,
}

app = FastAPI(
    title="CInBora API",
    description="API for CInBora",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters=swagger_ui_parameters,
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)

@app.get("/", summary="Hello world Endpoint", tags=["Root"])
async def root():
    return {"message": "Hello World"}

app.include_router(address_router, prefix="/address", tags=["Address"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="critical")