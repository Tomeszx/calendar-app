from datetime import datetime
from typing import List
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event as GoogleEvent
from googleapiclient.errors import HttpError

from models.api_event import EventCreate
from utilites.config_parser import get_config_data

ADMIN_EMAIL = get_config_data('google', 'admin_email')
CALENDAR_ID = get_config_data('google', 'calendar_id')


class GCalendar(GoogleCalendar):
    def __init__(self):
        super().__init__(CALENDAR_ID, credentials_path=get_config_data('google', 'path_to_secret'))

    def add_new_event(self, event: EventCreate) -> GoogleEvent:
        google_event = GoogleEvent(
            summary=f'{event.event_type} - {event.name}',
            start=event.start,
            end=event.end,
            description='',
            location=event.location,
            attendees=[ADMIN_EMAIL]
        )
        return self.add_event(google_event, send_updates='all')

    def get_google_events(self, from_date: datetime) -> List[GoogleEvent]:
        to_date = datetime(from_date.year + 5, from_date.month, from_date.day)
        return list(self.get_events(from_date, to_date, showDeleted=False))

    def delete_events(self, events_ids: List[str]) -> None:
        for event_id in events_ids:
            try:
                self.delete_event(event_id)
            except HttpError as e:
                if e.resp.status != 410:
                    raise e


def get_g_calendar() -> GCalendar:
    yield GCalendar()
