import uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Date, Time, String, Boolean, UUID


class Base(DeclarativeBase):
    pass


class DBEvent(Base):
    __tablename__ = "events"

    id : Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4, unique=True)
    google_id: Mapped[str] = mapped_column(String)
    date: Mapped[Date] = mapped_column(Date)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    start_time: Mapped[Time] = mapped_column(Time)
    location: Mapped[str] = mapped_column(String)
    event_type: Mapped[str] = mapped_column(String)
    confirmed: Mapped[bool] = mapped_column(Boolean)
