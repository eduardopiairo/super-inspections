from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/inspections", tags=["inspections"])


def _get_inspection_or_404(inspection_id: int, db: Session) -> models.Inspection:
    inspection = (
        db.query(models.Inspection)
        .options(joinedload(models.Inspection.answers))
        .filter(models.Inspection.id == inspection_id)
        .first()
    )
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")
    return inspection


@router.get("/", response_model=list[schemas.InspectionSummary])
def list_inspections(db: Session = Depends(get_db)):
    return db.query(models.Inspection).all()


@router.post("/", response_model=schemas.InspectionRead, status_code=201)
def create_inspection(inspection_in: schemas.InspectionCreate, db: Session = Depends(get_db)):
    template = db.get(models.Template, inspection_in.template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    inspection = models.Inspection(**inspection_in.model_dump())
    db.add(inspection)
    db.commit()
    db.refresh(inspection)
    return inspection


@router.get("/{inspection_id}", response_model=schemas.InspectionRead)
def get_inspection(inspection_id: int, db: Session = Depends(get_db)):
    return _get_inspection_or_404(inspection_id, db)


@router.patch("/{inspection_id}", response_model=schemas.InspectionRead)
def update_inspection(
    inspection_id: int, inspection_in: schemas.InspectionUpdate, db: Session = Depends(get_db)
):
    inspection = _get_inspection_or_404(inspection_id, db)

    if inspection_in.answers is not None:
        by_question = {answer.question_id: answer.value for answer in inspection_in.answers}
        existing = {answer.question_id: answer for answer in inspection.answers}
        for question_id, value in by_question.items():
            if question_id in existing:
                existing[question_id].value = value
            else:
                inspection.answers.append(
                    models.Answer(question_id=question_id, value=value)
                )

    if inspection_in.status is not None:
        inspection.status = inspection_in.status
        if inspection_in.status == "completed" and inspection.completed_at is None:
            inspection.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(inspection)
    return inspection


@router.delete("/{inspection_id}", status_code=204)
def delete_inspection(inspection_id: int, db: Session = Depends(get_db)):
    inspection = _get_inspection_or_404(inspection_id, db)
    db.delete(inspection)
    db.commit()
