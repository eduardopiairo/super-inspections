from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/sites", tags=["sites"])


@router.get("/", response_model=list[schemas.SiteRead])
def list_sites(db: Session = Depends(get_db)):
    return db.query(models.Site).all()


@router.post("/", response_model=schemas.SiteRead, status_code=201)
def create_site(site_in: schemas.SiteCreate, db: Session = Depends(get_db)):
    site = models.Site(**site_in.model_dump())
    db.add(site)
    db.commit()
    db.refresh(site)
    return site


@router.get("/{site_id}", response_model=schemas.SiteRead)
def get_site(site_id: int, db: Session = Depends(get_db)):
    site = db.get(models.Site, site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site
