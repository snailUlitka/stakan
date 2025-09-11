"""Module for connecting routers to the app."""

from fastapi import FastAPI

from stakan.api.v1.routes.storage import router

app = FastAPI(
    title="STAKAN",
    docs_url="/api/docs",
    version="0.1.0"
)

app.include_router(router=router, prefix="/storage")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
