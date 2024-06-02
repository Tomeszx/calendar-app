from calendar import monthrange
from datetime import date
from models.api_event import Event
from models.db_event import DBEvent
from pydantic import BaseModel
from typing import List, Tuple

from utilites.config_parser import get_config_data


class Day(BaseModel):
    month_index: int
    status: str
    date: str
    events: List[Event]
    max_events_num: int
    percentage_filled: str

    @classmethod
    def __get_events(cls, event_date: date, events: List[DBEvent], max_events: int) -> Tuple[List[Event], str, bool]:
        all_events = get_config_data('events_max_per_day')
        api_events = []
        status = 'busy-confirmed'
        for event in events:
            if event.start <= event_date <= event.end:
                api_events.append(Event(**event.__dict__))
                if not event.confirmed:
                    status = 'busy-not-confirmed'
                if all_events.get(event.event_type, '1') == '1':
                    return api_events, status, True

        if 0 < len(api_events) < max_events:
            status = status.replace('busy', 'free')
        return api_events, status, False

    @classmethod
    def create(cls, max_days: int, event_date: date, events: List[DBEvent], max_events: int):
        if not event_date or event_date.day > max_days:
            return Day(
                month_index=0, status='None', events=[], date='None',
                max_events_num=max_events, percentage_filled='0%'
            )

        data = dict(month_index=event_date.day, date=event_date.strftime("%Y.%m.%d"), max_events_num=max_events)
        api_events, status, is_daily_event = cls.__get_events(event_date, events, max_events)
        if is_daily_event:
            data['max_events_num'] = 1
        percentage_filled = f'{round((len(api_events) / data['max_events_num']) * 100)}%'
        if api_events:
            return Day(**data, status=status, events=api_events, percentage_filled=percentage_filled)
        return Day(**data, status='free', events=[], percentage_filled=percentage_filled)


class Month(BaseModel):
    days: List[Day]

    @classmethod
    def __get_total_count(cls, total) -> int:
        complete_weeks = (total + 6) // 7
        return complete_weeks * 7

    @classmethod
    def create(cls, events: List[DBEvent], given_date: date, max_events_num: str):
        start_index, max_days = monthrange(given_date.year, given_date.month)
        days = []

        for i in range(1, cls.__get_total_count(max_days + start_index) + 1):
            try:
                event_date = date(given_date.year, given_date.month, i - start_index)
            except ValueError:
                event_date = None
            days.append(Day.create(max_days, event_date, events, int(max_events_num)))
        return Month(days=days)
