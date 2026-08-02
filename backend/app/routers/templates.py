from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/templates", tags=["templates"])


def _build_template(template_in: schemas.TemplateCreate) -> models.Template:
    return models.Template(
        title=template_in.title,
        description=template_in.description,
        sections=[
            models.Section(
                title=section.title,
                order=section.order,
                questions=[
                    models.Question(**question.model_dump()) for question in section.questions
                ],
            )
            for section in template_in.sections
        ],
    )


def _get_template_or_404(template_id: int, db: Session) -> models.Template:
    template = (
        db.query(models.Template)
        .options(joinedload(models.Template.sections).joinedload(models.Section.questions))
        .filter(models.Template.id == template_id)
        .first()
    )
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.get("/", response_model=list[schemas.TemplateSummary])
def list_templates(db: Session = Depends(get_db)):
    return db.query(models.Template).all()


@router.post("/", response_model=schemas.TemplateRead, status_code=201)
def create_template(template_in: schemas.TemplateCreate, db: Session = Depends(get_db)):
    template = _build_template(template_in)
    db.add(template)
    db.commit()
    db.refresh(template)
    return template


@router.get("/{template_id}", response_model=schemas.TemplateRead)
def get_template(template_id: int, db: Session = Depends(get_db)):
    return _get_template_or_404(template_id, db)


@router.put("/{template_id}", response_model=schemas.TemplateRead)
def update_template(
    template_id: int, template_in: schemas.TemplateCreate, db: Session = Depends(get_db)
):
    template = _get_template_or_404(template_id, db)
    template.title = template_in.title
    template.description = template_in.description
    template.sections = _build_template(template_in).sections
    db.commit()
    db.refresh(template)
    return template


@router.delete("/{template_id}", status_code=204)
def delete_template(template_id: int, db: Session = Depends(get_db)):
    template = _get_template_or_404(template_id, db)
    db.delete(template)
    db.commit()
