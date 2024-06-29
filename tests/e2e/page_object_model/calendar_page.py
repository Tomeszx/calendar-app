import datetime
import time

from selenium.webdriver.common.by import By

from tests.e2e.page_object_model.base_page import BasePage, Locator


class CalendarPage(BasePage):
    event_selector_wedding = Locator(By.CSS_SELECTOR, '.tab[data-event="{}"]')
    event_selector_active = Locator(By.CLASS_NAME, 'tab.active')
    previous_month_button = Locator(By.CSS_SELECTOR, '#prev')
    next_month_button = Locator(By.CSS_SELECTOR, '#next')
    calendar_title = Locator(By.CSS_SELECTOR, '#monthYear')
    week_row = Locator(By.CSS_SELECTOR, '.week')
    day_cells = Locator(By.CSS_SELECTOR, '.week > button')
    day_cell = Locator(By.CSS_SELECTOR, 'button[name="{}"]')

    def __init__(self, driver):
        super().__init__(driver)

    def choose_event(self, event_name: str):
        self.wait_and_click(self.event_selector_wedding.format(event_name), timeout=5)

    def go_to_month(self, month: int, year: int):
        calendar_title = self.get_attribute(self.calendar_title, 'title').split('.')
        calendar_date = datetime.date(int(calendar_title[2]), int(calendar_title[1]), 1)
        if calendar_date > datetime.date(year, month, 1):
            button = self.previous_month_button
        else:
            button = self.next_month_button

        expected_month = f'{month}.{year}'
        start = time.time()
        while expected_month not in self.get_attribute(self.calendar_title, 'title'):
            self.wait_and_click(button)
            if time.time() - start > 10:
                raise TimeoutError(f'Timed out while moving to {expected_month}')

            self.wait_for_clickability(button)
            time.sleep(0.3)

    def check_displayed_calendar_title(self, expected_title: str):
        displayed_title = self.get_attribute(self.calendar_title, 'innerText')
        return displayed_title == expected_title, displayed_title

    def choose_date(self, date: datetime.date):
        date_string = date.strftime('%Y.%m.%d')
        self.wait_and_click(self.day_cell.format(date_string), timeout=5)
