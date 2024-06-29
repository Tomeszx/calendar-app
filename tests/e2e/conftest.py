import threading
import pytest
import time
import uvicorn

from datetime import datetime
from gcsa.event import Event as GoogleEvent
from main import app
from models.api_event import EventCreate
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from services.google_calendar import ADMIN_EMAIL, get_g_calendar
from tests.e2e.page_object_model.success_page import SuccessPage
from tests.e2e.page_object_model.base_page import BasePage
from tests.e2e.page_object_model.calendar_page import CalendarPage
from tests.e2e.page_object_model.form_page import FormPage
from typing import List
from utilites.config_parser import get_config_data


class MockGCalendar:
    def add_new_event(self, event: EventCreate) -> GoogleEvent:
        return GoogleEvent(
            event_id='12345',
            summary=f'{event.event_type} - {event.name}',
            start=event.start,
            end=event.end,
            description='',
            location=event.location,
            attendees=[ADMIN_EMAIL]
        )

    def get_google_events(self, from_date: datetime) -> List[GoogleEvent]:
        return []

    def delete_events(self, events_ids: List[str]) -> None:
        pass


def override_get_g_calendar() -> MockGCalendar:
    yield MockGCalendar()


app.dependency_overrides[get_g_calendar] = override_get_g_calendar


@pytest.fixture(scope='session', autouse=True)
def start_server(request: pytest.FixtureRequest):
    host = get_config_data('server_data', 'host')
    port = get_config_data('server_data', 'port')

    config = uvicorn.Config(app, host=host, port=port)
    server = uvicorn.Server(config)

    server_thread = threading.Thread(target=server.run, daemon=True)
    server_thread.start()

    def stop_server():
        server.should_exit = True
        server_thread.join()

    request.addfinalizer(stop_server)
    time.sleep(1)


class Pages:
    def __init__(self, driver: WebDriver):
        self.base_page = BasePage(driver)
        self.calendar_page = CalendarPage(driver)
        self.form_page = FormPage(driver)
        self.success_page = SuccessPage(driver)


class Context:
    def __init__(self, driver: WebDriver):
        self.pages = Pages(driver)


@pytest.fixture
def driver(request: pytest.FixtureRequest) -> WebDriver:
    options = Options()
    options.add_argument("--enable-automation")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--auto-open-devtools-for-tabs")
    options.page_load_strategy = "eager"
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    options.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(), options=options)
    request.addfinalizer(driver.quit)
    return driver


@pytest.fixture
def context(driver: WebDriver) -> Context:
    return Context(driver)
