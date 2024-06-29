from __future__ import annotations

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utilites.config_parser import get_config_data


class Locator:
    def __init__(self, locator_type: str = By.XPATH, arg: str = None):
        self.value: tuple[str, str] = locator_type, arg

    def __iter__(self) -> tuple[By, str]:
        yield from self.value

    def __getitem__(self, item):
        return self.value[item]

    def format(self, format_option: str) -> Locator:
        return Locator(self.value[0], arg=self.value[1].format(format_option))


class BasePage:
    def __init__(self, driver: WebDriver):
        self.base_url = get_config_data('urls', 'main_page')
        self.driver = driver

    def open(self, website: str = ''):
        return self.driver.get(f'{self.base_url}{website}')

    def switch_to_frame(self, frame: Locator) -> None:
        new_frame = self.driver.find_element(*frame)
        self.driver.switch_to.frame(new_frame)

    def get_element(self, locator):
        return self.driver.find_element(*locator)

    def get_elements(self, locator):
        return self.driver.find_elements(*locator)

    def is_element_exists(self, locator: Locator, timeout=5) -> bool:
        if timeout == 0:
            return bool(self.get_elements(locator))
        try:
            self.wait_for_visibility(locator, timeout)
        except TimeoutException:
            return False
        return True

    def get_attribute(self, locator, attribute_name):
        return self.get_element(locator).get_attribute(attribute_name)

    def wait_and_click(self, locator: Locator, timeout: int = 15) -> None:
        self.wait_for_clickability(locator, timeout).click()

    def enter_text(self, locator, value):
        self.get_element(locator).send_keys(value)

    def wait_for_visibility(self, locator: Locator, timeout=15) -> WebElement:
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator),
                                                         f"Element {locator} is not visible after {timeout}s")

    def wait_for_clickability(self, locator: Locator, timeout=15) -> WebElement:
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator.value),
                                                         f"Element {locator} is not clickable after {timeout}s")
