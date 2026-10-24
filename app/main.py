from fastapi import FastAPI

from app.routers import vehicles

app = FastAPI(
    title="Car Agency API",
    description="Catalog of used vehicles for sale, including vehicles that need repair or are sold for parts.",
    version="0.1.0",
)

app.include_router(vehicles.router)


@app.get("/", tags=["health"])
def root():
    return {"status": "ok"}
