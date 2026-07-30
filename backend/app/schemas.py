from pydantic import BaseModel


class InspectionBase(BaseModel):
    title: str
    status: str = "pending"


class InspectionCreate(InspectionBase):
    pass


class InspectionRead(InspectionBase):
    id: int

    class Config:
        from_attributes = True
