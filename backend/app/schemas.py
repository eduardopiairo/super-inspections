from datetime import date, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel


# --- Users & Sites ---


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


class SiteBase(BaseModel):
    name: str


class SiteCreate(SiteBase):
    pass


class SiteRead(SiteBase):
    id: int

    class Config:
        from_attributes = True


# --- Templates ---


class ResponseType(str, Enum):
    yes_no = "yes_no"
    multiple_choice = "multiple_choice"
    text = "text"
    photo = "photo"
    signature = "signature"
    date = "date"


class QuestionBase(BaseModel):
    text: str
    response_type: ResponseType = ResponseType.yes_no
    options: list[str] | None = None
    required: bool = True
    order: int = 0


class QuestionCreate(QuestionBase):
    pass


class QuestionRead(QuestionBase):
    id: int

    class Config:
        from_attributes = True


class SectionBase(BaseModel):
    title: str
    order: int = 0


class SectionCreate(SectionBase):
    questions: list[QuestionCreate] = []


class SectionRead(SectionBase):
    id: int
    questions: list[QuestionRead] = []

    class Config:
        from_attributes = True


class TemplateBase(BaseModel):
    title: str
    description: str = ""


class TemplateCreate(TemplateBase):
    sections: list[SectionCreate] = []


class TemplateRead(TemplateBase):
    id: int
    sections: list[SectionRead] = []

    class Config:
        from_attributes = True


class TemplateSummary(TemplateBase):
    id: int

    class Config:
        from_attributes = True


# --- Inspections & Answers ---


class AnswerBase(BaseModel):
    question_id: int
    value: Any = None


class AnswerCreate(AnswerBase):
    pass


class AnswerRead(AnswerBase):
    id: int

    class Config:
        from_attributes = True


class InspectionBase(BaseModel):
    template_id: int
    title: str
    site_id: int | None = None
    assigned_user_id: int | None = None


class InspectionCreate(InspectionBase):
    pass


class InspectionUpdate(BaseModel):
    status: str | None = None
    answers: list[AnswerCreate] | None = None


class InspectionRead(InspectionBase):
    id: int
    schedule_id: int | None = None
    status: str
    created_at: datetime
    completed_at: datetime | None = None
    answers: list[AnswerRead] = []

    class Config:
        from_attributes = True


class InspectionSummary(InspectionBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class RecurrenceFrequency(str, Enum):
    once = "once"
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"


# --- Schedules ---


class ScheduleBase(BaseModel):
    template_id: int
    frequency: RecurrenceFrequency = RecurrenceFrequency.once
    start_date: date
    site_id: int | None = None
    assigned_user_id: int | None = None
    active: bool = True


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleRead(ScheduleBase):
    id: int

    class Config:
        from_attributes = True


# --- Actions ---


class ActionStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    done = "done"


class ActionBase(BaseModel):
    inspection_id: int | None = None
    question_id: int | None = None
    site_id: int | None = None
    description: str
    status: ActionStatus = ActionStatus.open
    assigned_user_id: int | None = None
    due_date: date | None = None
    frequency: RecurrenceFrequency = RecurrenceFrequency.once


class ActionCreate(ActionBase):
    pass


class ActionUpdate(BaseModel):
    description: str | None = None
    status: ActionStatus | None = None
    assigned_user_id: int | None = None
    due_date: date | None = None
    frequency: RecurrenceFrequency | None = None


class ActionRead(ActionBase):
    id: int

    class Config:
        from_attributes = True
