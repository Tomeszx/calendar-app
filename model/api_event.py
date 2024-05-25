import datetime

from fastapi.params import Form
from pydantic import BaseModel, EmailStr


class Event(BaseModel):
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
