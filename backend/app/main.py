from fastapi import FastAPI

from app.database import Base, engine
from app.routers import inspections

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Super Inspections API")

app.include_router(inspections.router)


@app.get("/health")
def health():
    return {"status": "ok"}
