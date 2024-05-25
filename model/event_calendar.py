from calendar import monthrange
from datetime import date
from model.api_event import Event
from model.db_event import DBEvent
from pydantic import BaseModel
from typing import List


class Day(BaseModel):
    month_index: int
    status: str | None
    event: Event | None
    date: str | None

    @classmethod
    def create(cls, max_days: int, event_date: date, events: dict[date, DBEvent]):
        if not event_date or event_date.day > max_days:
            return Day(month_index=0, status='None', event=None, date=event_date)
        data = dict(month_index=event_date.day, date=event_date.strftime("%Y.%m.%d"))
        if event := events.get(event_date):
            if event.confirmed:
                return Day(**data, status='confirmed', event=Event(**event.__dict__))
            return Day(**data, status='not-confirmed', event=Event(**event.__dict__))
        return Day(**data, status='free', event=None)


class Week(BaseModel):
    days: List[Day]

    @classmethod
    def create(cls, week: int, start_index: int, max_days: int, given_date: date, events: dict[date, DBEvent]):
        days = []
        for i in range(week, week + 7):
            try:
                event_date = date(given_date.year, given_date.month, i - start_index)
            except ValueError:
                event_date = None
            days.append(Day.create(max_days, event_date, events))
        return Week(days=days)


class Month(BaseModel):
    weeks: List[Week]

    @classmethod
    def create(cls, events: dict[date, DBEvent], given_date: date):
        start_index, max_days = monthrange(given_date.year, given_date.month)
        weeks = []
        for i in range(1, max_days + start_index + 1, 7):
            weeks.append(Week.create(i, start_index, max_days, given_date, events))
        return Month(weeks=weeks)
