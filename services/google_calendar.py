from datetime import datetime
from typing import Iterable, List
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event as GoogleEvent
from googleapiclient.errors import HttpError

from model.api_event import Event as ApiEvent
from utilites.config_parser import get_config_data


ADMIN_EMAIL = get_config_data('google', 'admin_email')
CALENDAR_ID = get_config_data('google', 'calendar_id')


def add_event(event: ApiEvent) -> GoogleEvent:
    calendar = GoogleCalendar(CALENDAR_ID, credentials_path=get_config_data('google', 'path_to_secret'))
    google_event = GoogleEvent(
        f'{event.event_type} with {event.name}',
        start=datetime(event.date.year, event.date.month, event.date.day, hour=event.start_time.hour - 3),
        end=datetime(event.date.year, event.date.month, event.date.day, hour=23, minute=59, second=59),
        description='',
        location=event.location,
        attendees=[ADMIN_EMAIL]
    )
    return calendar.add_event(google_event, send_updates='all')


def get_events(from_date: datetime) -> List[GoogleEvent]:
    calendar = GoogleCalendar(CALENDAR_ID, credentials_path=get_config_data('google', 'path_to_secret'))
    to_date = datetime(from_date.year + 5, from_date.month, from_date.day)
    return list(calendar.get_events(from_date, to_date, showDeleted=False))


def delete_events(events_ids: List[str]) -> None:
    for event_id in events_ids:
        calendar = GoogleCalendar(CALENDAR_ID, credentials_path=get_config_data('google', 'path_to_secret'))
        try:
            calendar.delete_event(event_id)
        except HttpError as e:
            if e.resp.status != 410:
                raise e
