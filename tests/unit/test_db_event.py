from datetime import datetime, timedelta

from db.event import get_all_future_events, create_db_event, update_db_events, get_event_by_id, delete_db_events
from gcsa.attendee import Attendee
from gcsa.event import Event as GoogleEvent
from models.api_event import EventCreate
from tests.db_test_data import get_test_data
from tests.conftest import override_get_db
from utilites.config_parser import get_config_data


TEST_DATA = get_test_data()


def test_get_event_by_id():
    db = next(override_get_db())
    event = get_event_by_id(TEST_DATA[0].google_event_id, db)
    expected_event = TEST_DATA[0]
    assert expected_event == event, f'The events are not the same {expected_event.__dict__=} {event.__dict__=}'


def test_get_all_future_events():
    db = next(override_get_db())
    events = get_all_future_events(datetime.today().date(), db)
    for event, expected_event in zip(events, TEST_DATA, strict=True):
        assert event == expected_event


def test_create_db_event():
    db = next(override_get_db())
    today = datetime.today()
    expected_event = EventCreate.as_form(
        date=(datetime(today.year, today.month, today.day) + timedelta(weeks=10)).strftime('%Y.%m.%d'),
        name='Test3',
        email='test@gmail.com',
        location='Warszawa, Hoża 51',
        event_type='wesele',
    )
    event = create_db_event(expected_event, google_event_id='Test3', session=db)

    assert event.start == expected_event.start, f'{event.start=} != {expected_event.start=}'
    assert event.end == expected_event.end, f'{event.end=} != {expected_event.end=}'
    assert event.event_type == expected_event.event_type, f'{event.event_type=} != {expected_event.event_type=}'
    assert event.location == expected_event.location, f'{event.location=} != {expected_event.location=}'
    assert event.name == expected_event.name, f'{event.name=} != {expected_event.name=}'
    assert event.email == expected_event.email, f'{event.email=} != {expected_event.email=}'


def test_update_db_events():
    db = next(override_get_db())
    attendee = Attendee(email=get_config_data('google', 'admin_email'))
    attendee.response_status = 'accepted'
    google_events = []
    for event in TEST_DATA:
        google_events.append(GoogleEvent(
            event_id=event.google_event_id,
            summary=f"{event.event_type} - {event.name}",
            start=event.start,
            end=event.end,
            location=event.location,
            attendees=[attendee]
        ))
    update_db_events(google_events, db)

    for event in TEST_DATA:
        db_event = get_event_by_id(event.google_event_id, db)
        assert db_event.confirmed is True, 'The event should be confirmed'


def test_delete_db_event_after_accept():
    db = next(override_get_db())
    attendee = Attendee(email=get_config_data('google', 'admin_email'))
    attendee.response_status = 'accepted'
    google_events = []
    for event in TEST_DATA:
        google_events.append(GoogleEvent(
            event_id=event.google_event_id,
            summary=f"{event.event_type} - {event.name}",
            start=event.start,
            end=event.end,
            location=event.location,
            attendees=[attendee]
        ))

    delete_db_events(google_events, db)

    for event in TEST_DATA:
        db_event = get_event_by_id(event.google_event_id, db)
        assert db_event, 'The event should not be deleted'


def test_delete_db_event_after_decline():
    db = next(override_get_db())
    attendee = Attendee(email=get_config_data('google', 'admin_email'))
    attendee.response_status = 'declined'
    google_events = []
    for event in TEST_DATA:
        google_events.append(GoogleEvent(
            event_id=event.google_event_id,
            summary=f"{event.event_type} - {event.name}",
            start=event.start,
            end=event.end,
            location=event.location,
            attendees=[attendee]
        ))

    delete_db_events(google_events, db)

    for event in TEST_DATA:
        db_event = get_event_by_id(event.google_event_id, db)
        assert not db_event, 'The event should be deleted'


def test_delete_db_event_after_removing_from_google_calendar():
    db = next(override_get_db())
    delete_db_events([], db)

    for event in TEST_DATA:
        db_event = get_event_by_id(event.google_event_id, db)
        assert not db_event, 'The event should be deleted'
