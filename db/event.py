from datetime import date, datetime, timedelta
from typing import List, Iterable
from sqlalchemy.orm import Session

from utilites.config_parser import get_config_data
from model.api_event import Event
from model.db_event import DBEvent
from gcsa.event import Event as GoogleEvent


def get_all_future_events(start_date: date, session: Session) -> dict[date, DBEvent]:
    events = session.query(DBEvent).filter(DBEvent.date >= start_date)
    return {event.date: event for event in events}


def create_db_event(event: Event, google_id: str, session: Session) -> DBEvent:
    db_event = DBEvent(**event.__dict__, google_id=google_id)
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event


def __create_event(event: GoogleEvent, start_date: datetime, session: Session) -> None:
    attendee = event.attendees[0]
    db_event = DBEvent(
        date=start_date.date(),
        name=attendee.display_name or '',
        email=attendee.email,
        start_time=start_date.time(),
        location=event.location or '',
        event_type=event.other['eventType'],
        confirmed=attendee.response_status == 'confirmed',
        google_id=event.event_id
    )
    session.add(db_event)


def __split_each_day_to_new_db_entry(event: GoogleEvent, db_events: dict[date, DBEvent], session: Session) -> None:
    for day in range((event.end - event.start).days):
        event_date = event.start + timedelta(days=day)
        start_date = datetime(event_date.year, event_date.month, event_date.day)
        db_event = db_events.get(start_date.date())
        if not db_event and start_date.date() >= date.today():
            __create_event(event, start_date, session)
            continue
        elif db_event:
            attendee = event.attendees[0]
            if attendee.email == get_config_data('google', 'admin_email'):
                if attendee.response_status == 'accepted' and not db_event.confirmed:
                    setattr(db_event, 'confirmed', True)
                elif attendee.response_status == 'declined':
                    session.delete(db_event)


def update_db_events(events: Iterable[GoogleEvent], session: Session) -> None:
    db_events = get_all_future_events(date.today(), session)
    for event in events:
        end_date = event.end
        if (end_date - event.start).days == 0:
            end_date += timedelta(days=1)
        __split_each_day_to_new_db_entry(event, db_events, session)
    session.commit()


def delete_db_events(events_list: Iterable[GoogleEvent], session: Session) -> List[str]:
    db_events = get_all_future_events(date.today(), session)
    deleted_events = []
    for db_event in db_events.values():
        result: List[GoogleEvent] = list(filter(lambda event: event.event_id == db_event.google_id, events_list))
        if not result or result[0].attendees[0].response_status == 'declined':
            session.delete(db_event)
            deleted_events.append(db_event.google_id)
    session.commit()
    return deleted_events
