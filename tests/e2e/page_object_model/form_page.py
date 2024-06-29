from selenium.webdriver.common.by import By
from tests.e2e.page_object_model.base_page import BasePage, Locator


class FormPage(BasePage):
    from_iframe = Locator(By.CSS_SELECTOR, '#iframeContent')
    first_step_title = Locator(By.CSS_SELECTOR, '#first-step-title')
    first_step_subtitle = Locator(By.CSS_SELECTOR, '#first-step-subtitle')
    date_input = Locator(By.CSS_SELECTOR, 'input[name="date"]')
    event_type_input = Locator(By.CSS_SELECTOR, 'input[name="event_type"]')
    name_input = Locator(By.CSS_SELECTOR, 'input[name="name"]')
    email_input = Locator(By.CSS_SELECTOR, 'input[name="email"]')
    location_input = Locator(By.CSS_SELECTOR, 'input[name="location"]')
    submit_button = Locator(By.CSS_SELECTOR, 'button[type="submit"]')

    def __init__(self, driver):
        super().__init__(driver)

    def switch_to_form(self):
        self.switch_to_frame(self.from_iframe)

    def book_event(self, name: str, email: str, location: str) -> None:
        self.enter_text(self.name_input, name)
        self.enter_text(self.email_input, email)
        self.enter_text(self.location_input, location)
        self.wait_and_click(self.submit_button, 5)
