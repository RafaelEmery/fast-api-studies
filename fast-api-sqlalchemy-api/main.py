from fastapi import FastAPI

from api.api import router as api_router


app = FastAPI(title="FastAPI with SQLAlchemy Async Endpoints")
app.include_router(api_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000, log_level="info", reload=True)
