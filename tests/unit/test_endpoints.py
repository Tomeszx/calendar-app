from datetime import datetime, timedelta

from tests.conftest import client


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200, f'{response.text=}'


def test_create_event():
    event = dict(
        name='Tomasz',
        email='tomasz_test@gmail.com',
        date=(datetime.today() + timedelta(days=9)).strftime('%Y.%m.%d'),
        event_type='wesele',
        location='Hoża 51, Warszawa',
    )
    response = client.post('/event', data=event)
    assert response.status_code == 200, response.text


def test_get_all_events_with_missing_params():
    params = {
        "missing_event_param": "?month=05&year=2024",
        "missing_year_param": "?month=05&event=wesele",
        "missing_month_param": "?year=2024&event=wesele",
        "no_params": "",
    }
    for title, param in params.items():
        response = client.get(f"/calendar{param}")
        assert response.status_code == 422, f'the response status is not valid for {title=}. {response.text=}'


def test_get_all_events():
    response = client.get("/calendar?month=05&year=2024&event=wesele")
    assert response.status_code == 200, response.text
