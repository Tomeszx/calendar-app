from calendar import monthrange
from datetime import date
from model.api_event import Event
from model.db_event import DBEvent
from pydantic import BaseModel
from typing import List, Tuple


class Day(BaseModel):
    month_index: int
    status: str
    events: List[Event]
    date: str

    @classmethod
    def __get_events(cls, event_date: date, events: List[DBEvent]) -> Tuple[List[Event], str]:
        api_events = []
        confirmed = 'confirmed'
        for event in events:
            if event.start <= event_date <= event.end:
                api_events.append(Event(**event.__dict__))
                if not event.confirmed:
                    confirmed = 'not-confirmed'
        return api_events, confirmed

    @classmethod
    def create(cls, max_days: int, event_date: date, events: List[DBEvent]):
        if not event_date or event_date.day > max_days:
            return Day(month_index=0, status='None', events=[], date='None')

        data = dict(month_index=event_date.day, date=event_date.strftime("%Y.%m.%d"))
        api_events, status = cls.__get_events(event_date, events)
        if api_events:
            return Day(**data, status=status, events=api_events)
        return Day(**data, status='free', events=[])


class Month(BaseModel):
    days: List[Day]

    @classmethod
    def __get_total_count(cls, total) -> int:
        complete_weeks = (total + 6) // 7
        return complete_weeks * 7

    @classmethod
    def create(cls, events: List[DBEvent], given_date: date):
        start_index, max_days = monthrange(given_date.year, given_date.month)
        days = []

        for i in range(1, cls.__get_total_count(max_days + start_index) + 1):
            try:
                event_date = date(given_date.year, given_date.month, i - start_index)
            except ValueError:
                event_date = None
            days.append(Day.create(max_days, event_date, events))
        return Month(days=days)
