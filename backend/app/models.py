from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)


class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, default="")

    sections = relationship(
        "Section", back_populates="template", cascade="all, delete-orphan", order_by="Section.order"
    )


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=False)
    title = Column(String, nullable=False)
    order = Column(Integer, default=0)

    template = relationship("Template", back_populates="sections")
    questions = relationship(
        "Question", back_populates="section", cascade="all, delete-orphan", order_by="Question.order"
    )


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)
    text = Column(String, nullable=False)
    response_type = Column(String, nullable=False, default="yes_no")
    options = Column(JSON, nullable=True)
    required = Column(Boolean, default=True)
    order = Column(Integer, default=0)

    section = relationship("Section", back_populates="questions")


class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=False)
    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=True)
    assigned_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    title = Column(String, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    template = relationship("Template")
    schedule = relationship("Schedule", back_populates="inspections")
    site = relationship("Site")
    assigned_user = relationship("User")
    answers = relationship("Answer", back_populates="inspection", cascade="all, delete-orphan")
    actions = relationship("Action", back_populates="inspection", cascade="all, delete-orphan")


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    value = Column(JSON, nullable=True)

    inspection = relationship("Inspection", back_populates="answers")
    question = relationship("Question")


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=False)
    frequency = Column(String, nullable=False, default="once")
    start_date = Column(Date, nullable=False)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=True)
    assigned_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    active = Column(Boolean, default=True)

    template = relationship("Template")
    site = relationship("Site")
    assigned_user = relationship("User")
    inspections = relationship("Inspection", back_populates="schedule")


class Action(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"), nullable=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=True)
    description = Column(String, nullable=False)
    status = Column(String, default="open")
    assigned_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    due_date = Column(Date, nullable=True)
    frequency = Column(String, nullable=False, default="once")

    inspection = relationship("Inspection", back_populates="actions")
    question = relationship("Question")
    site = relationship("Site")
    assigned_user = relationship("User")
