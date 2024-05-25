from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Date, Time, String, Boolean


class Event(BaseModel):
    data: Optional[dict] = None


class EventCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ResponseCreate(BaseModel):
    status: str
    msg: str
    data: EventCreate | None


class EventUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    description: Optional[str] = None


class Base(DeclarativeBase):
    pass


class DBEvent(Base):
    __tablename__ = "events"

    date: Mapped[Date] = mapped_column(Date, primary_key=True, index=True)
    google_id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    start_time: Mapped[Time] = mapped_column(Time)
    location: Mapped[str] = mapped_column(String)
    event_type: Mapped[str] = mapped_column(String)
    confirmed: Mapped[bool] = mapped_column(Boolean)
