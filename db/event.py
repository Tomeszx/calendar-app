from datetime import date, datetime, timedelta
from functools import partial
from typing import List, Iterable
from sqlalchemy.orm import Session

from utilites.config_parser import get_config_data
from model.api_event import Event, EventCreate
from model.db_event import DBEvent
from gcsa.event import Event as GoogleEvent


def get_all_future_events(start_date: date, session: Session) -> List[DBEvent]:
    return list(session.query(DBEvent).filter(DBEvent.start >= start_date))


def create_db_event(event: EventCreate, google_event_id: str, session: Session) -> DBEvent:
    db_event = DBEvent(**event.__dict__, google_event_id=google_event_id)
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event


def __process_event_status(event: GoogleEvent, db_event: DBEvent, session: Session) -> None:
    attendee = event.attendees[0]
    if attendee.email == get_config_data('google', 'admin_email'):
        if attendee.response_status == 'accepted' and not db_event.confirmed:
            setattr(db_event, 'confirmed', True)
        elif attendee.response_status == 'declined':
            session.delete(db_event)


def __create_event(event: GoogleEvent, session: Session) -> None:
    attendee = event.attendees[0]
    db_event = DBEvent(
        start=event.start,
        end=event.end - timedelta(days=1),
        name=attendee.display_name or '',
        email=attendee.email,
        location=event.location or '',
        event_type=event.other['eventType'],
        confirmed=attendee.response_status == 'confirmed',
        google_event_id=event.event_id
    )
    session.add(db_event)


def update_db_events(events: Iterable[GoogleEvent], session: Session) -> None:
    db_events = list(session.query(DBEvent).filter(DBEvent.start >= date.today()))
    for event in events:
        db_event = next(filter(lambda e: e.google_event_id == event.event_id, db_events), None)
        if db_event:
            __process_event_status(event, db_event, session)
        else:
            __create_event(event, session)
    session.commit()


def delete_db_events(events_list: Iterable[GoogleEvent], session: Session) -> List[str]:
    db_events = session.query(DBEvent).filter(DBEvent.start >= date.today())
    deleted_events = []
    for db_event in db_events:
        result: List[GoogleEvent] = list(filter(lambda event: event.event_id == db_event.google_event_id, events_list))
        if not result or result[0].attendees[0].response_status == 'declined':
            session.delete(db_event)
            deleted_events.append(db_event.google_event_id)
    session.commit()
    return deleted_events
