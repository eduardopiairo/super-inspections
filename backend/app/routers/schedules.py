from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/schedules", tags=["schedules"])


@router.get("/", response_model=list[schemas.ScheduleRead])
def list_schedules(db: Session = Depends(get_db)):
    return db.query(models.Schedule).all()


@router.post("/", response_model=schemas.ScheduleRead, status_code=201)
def create_schedule(schedule_in: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    template = db.get(models.Template, schedule_in.template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    schedule = models.Schedule(**schedule_in.model_dump())
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule


@router.get("/{schedule_id}", response_model=schemas.ScheduleRead)
def get_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.get(models.Schedule, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule


@router.delete("/{schedule_id}", status_code=204)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.get(models.Schedule, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    db.delete(schedule)
    db.commit()
