from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/actions", tags=["actions"])


@router.get("/", response_model=list[schemas.ActionRead])
def list_actions(db: Session = Depends(get_db)):
    return db.query(models.Action).all()


@router.post("/", response_model=schemas.ActionRead, status_code=201)
def create_action(action_in: schemas.ActionCreate, db: Session = Depends(get_db)):
    if action_in.inspection_id is not None and not db.get(
        models.Inspection, action_in.inspection_id
    ):
        raise HTTPException(status_code=404, detail="Inspection not found")

    if action_in.question_id is not None and action_in.inspection_id is None:
        raise HTTPException(
            status_code=422, detail="question_id requires an inspection_id"
        )

    if action_in.site_id is not None and not db.get(models.Site, action_in.site_id):
        raise HTTPException(status_code=404, detail="Site not found")

    action = models.Action(**action_in.model_dump())
    db.add(action)
    db.commit()
    db.refresh(action)
    return action


@router.get("/{action_id}", response_model=schemas.ActionRead)
def get_action(action_id: int, db: Session = Depends(get_db)):
    action = db.get(models.Action, action_id)
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    return action


@router.patch("/{action_id}", response_model=schemas.ActionRead)
def update_action(action_id: int, action_in: schemas.ActionUpdate, db: Session = Depends(get_db)):
    action = db.get(models.Action, action_id)
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")

    for field, value in action_in.model_dump(exclude_unset=True).items():
        setattr(action, field, value)

    db.commit()
    db.refresh(action)
    return action


@router.delete("/{action_id}", status_code=204)
def delete_action(action_id: int, db: Session = Depends(get_db)):
    action = db.get(models.Action, action_id)
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    db.delete(action)
    db.commit()
