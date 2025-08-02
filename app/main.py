import uvicorn
from fastapi import FastAPI
from starlette_prometheus import PrometheusMiddleware, metrics

from app.routes.user import router as user_router
from app.routes.travel import router as travel_router
from app.database import create_db_and_tables


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

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(travel_router, prefix="/travel", tags=["Travel"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="critical")
