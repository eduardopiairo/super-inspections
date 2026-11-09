from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

from app.database import Base, engine
from app.routers import actions, inspections, schedules, sites, templates, users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Super Inspections API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(templates.router)
app.include_router(inspections.router)
app.include_router(schedules.router)
app.include_router(actions.router)
app.include_router(users.router)
app.include_router(sites.router)


@app.get("/health")
def health():
    return {"status": "ok"}

