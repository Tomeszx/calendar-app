import datetime
from uuid import UUID

from fastapi.params import Form
from pydantic import BaseModel, EmailStr


class Event(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    date: datetime.date
    start_time: datetime.time
    event_type: str
    location: str
    confirmed: bool = False

    @classmethod
    def as_form(
            cls,
            id: UUID = Form(...),
            name: str = Form(1),
            email: EmailStr = Form(2),
            date: str = Form(3),
            start_time: datetime.time = Form(4),
            event_type: str = Form(5),
            location: str = Form(6),
    ):
        return cls(
            id=id,
            name=name,
            email=email,
            date=datetime.datetime.strptime(date, "%Y.%m.%d"),
            start_time=start_time,
            event_type=event_type,
            location=location,
        )


class EventCreate(BaseModel):
    name: str
    email: EmailStr
    date: datetime.date
    start_time: datetime.time
    event_type: str
    location: str
    confirmed: bool = False

    @classmethod
    def as_form(
            cls,
            name: str = Form(...),
            email: EmailStr = Form(1),
            date: str = Form(2),
            start_time: datetime.time = Form(3),
            event_type: str = Form(4),
            location: str = Form(5),
    ):
        return cls(
            name=name,
            email=email,
            date=datetime.datetime.strptime(date, "%Y.%m.%d"),
            start_time=start_time,
            event_type=event_type,
            location=location,
        )
