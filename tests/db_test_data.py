from datetime import datetime, timedelta
from models.db_event import DBEvent


def get_test_data():
    today = datetime.today()
    return [
        DBEvent(
            google_event_id='Test1',
            start=today.date(),
            end=today.date(),
            name='Test1',
            email='test@gmail.com',
            location='Warszawa, Hoża 51',
            event_type='wesele',
            confirmed=False
        ),
        DBEvent(
            google_event_id='Test2',
            start=(datetime(today.year, today.month, today.day) + timedelta(days=2)).date(),
            end=(datetime(today.year, today.month, today.day) + timedelta(days=4)).date(),
            name='Test2',
            email='test@gmail.com',
            location='Warszawa, Hoża 51',
            event_type='wesele',
            confirmed=True
        )
    ]
