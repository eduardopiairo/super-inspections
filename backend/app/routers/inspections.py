from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/inspections", tags=["inspections"])


@router.get("/", response_model=list[schemas.InspectionRead])
def list_inspections(db: Session = Depends(get_db)):
    return db.query(models.Inspection).all()


@router.post("/", response_model=schemas.InspectionRead, status_code=201)
def create_inspection(inspection: schemas.InspectionCreate, db: Session = Depends(get_db)):
    db_inspection = models.Inspection(**inspection.model_dump())
    db.add(db_inspection)
    db.commit()
    db.refresh(db_inspection)
    return db_inspection


@router.get("/{inspection_id}", response_model=schemas.InspectionRead)
def get_inspection(inspection_id: int, db: Session = Depends(get_db)):
    inspection = db.get(models.Inspection, inspection_id)
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")
    return inspection
