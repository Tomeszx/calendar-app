from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Date, String, Boolean


class Base(DeclarativeBase):
    pass


class DBEvent(Base):
    __tablename__ = "events"

    google_event_id: Mapped[str] = mapped_column(String, primary_key=True, unique=True)
    start: Mapped[Date] = mapped_column(Date)
    end: Mapped[Date] = mapped_column(Date)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    location: Mapped[str] = mapped_column(String)
    event_type: Mapped[str] = mapped_column(String)
    confirmed: Mapped[bool] = mapped_column(Boolean)
