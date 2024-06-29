import datetime

from fastapi.params import Form
from pydantic import BaseModel, EmailStr


class Event(BaseModel):
    google_event_id: str
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
            google_event_id: str = Form(...),
            name: str = Form(...),
            email: EmailStr = Form(...),
            event_type: str = Form(...),
            date: str = Form(...),
            location: str = Form(...),
    ):
        start_date = datetime.datetime.strptime(date, "%Y.%m.%d").date()
        end_date = start_date
        return cls(
            google_event_id=google_event_id,
            name=name,
            email=email,
            start=start_date,
            end=end_date,
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
            email: EmailStr = Form(...),
            event_type: str = Form(...),
            date: str = Form(...),
            location: str = Form(...),
    ):
        start_date = datetime.datetime.strptime(date, "%Y.%m.%d").date()
        end_date = start_date
        return cls(
            name=name,
            email=email,
            start=start_date,
            end=end_date,
            event_type=event_type,
            location=location,
        )
