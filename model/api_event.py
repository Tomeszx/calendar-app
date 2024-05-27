import datetime
from uuid import UUID

from fastapi.params import Form
from pydantic import BaseModel, EmailStr


class Event(BaseModel):
    google_event_id: str
    name: str
    email: EmailStr
    start: datetime.date
    end: datetime.date
    event_type: str
    location: str
    confirmed: bool = False

    @classmethod
    def as_form(
            cls,
            google_event_id: UUID = Form(...),
            name: str = Form(1),
            email: EmailStr = Form(2),
            date: str = Form(3),
            start_time: datetime.time = Form(4),
            event_type: str = Form(5),
            location: str = Form(6),
    ):
        return cls(
            google_event_id=google_event_id,
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
    start: datetime.date | datetime.datetime
    end: datetime.date | datetime.datetime
    event_type: str
    location: str
    confirmed: bool = False

    @classmethod
    def as_form(
            cls,
            name: str = Form(...),
            email: EmailStr = Form(1),
            start: str = Form(2),
            event_type: str = Form(4),
            location: str = Form(5),
    ):
        start_date = datetime.datetime.strptime(start, "%Y.%m.%d").date()
        end_date = start_date
        return cls(
            name=name,
            email=email,
            start=start_date,
            end=end_date,
            event_type=event_type,
            location=location,
        )
