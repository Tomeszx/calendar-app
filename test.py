from datetime import datetime

import requests

if __name__ == '__main__':
    payload = dict(
        name='Tomasz',
        email='tomek123@gmail.com',
        date=datetime(2024, 5, 20).strftime('%Y-%m-%d'),
        start_time=datetime.today().strftime('%H:%M:%S'),
        street='Wolna 13',
        city='Warszawa',
        state='Mazowieckie',
        zip_code='22-424',
        country='Polska',
        event_type='Wesele'
    )
    r = requests.post('http://127.0.0.1:8000/event/create', json=payload)
    print(r.text)