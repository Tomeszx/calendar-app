from selenium.webdriver.common.by import By

from tests.e2e.page_object_model.base_page import BasePage, Locator


class SuccessPage(BasePage):
    success_header = Locator(By.CSS_SELECTOR, '#success-header')

    def __init__(self, driver):
        super().__init__(driver)

    def is_success_header_displayed(self) -> bool:
        if not self.is_element_exists(self.success_header):
            return False
        return self.get_element(self.success_header).is_displayed()
