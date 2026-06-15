from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Page:
    BASE_URL = 'https://soft.reelly.io'

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout=10)

    def open_url(self, end_url=''):
        self.driver.get(f'{self.BASE_URL}/{end_url}')

    def get_current_url(self):
        return self.driver.current_url

    def find_element(self, *locator):
        return self.driver.find_element(*locator)

    def find_elements(self, *locator):
        return self.driver.find_elements(*locator)

    def click(self, *locator):
        self.find_element(*locator).click()

    def input_text(self, text, *locator):
        field = self.find_element(*locator)
        field.clear()
        field.send_keys(text)

    def refresh_page(self):
        self.driver.refresh()

    def wait_until_appear(self, *locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator),
            message=f'Element by {locator} is not visible'
        )

    def wait_until_visible(self, *locator):
        return self.wait_until_appear(*locator)

    def wait_until_clickable(self, *locator):
        return self.wait.until(
            EC.element_to_be_clickable(locator),
            message=f'Element by {locator} is not clickable'
        )

    def wait_until_clickable_click(self, *locator):
        element = self.wait_until_clickable(*locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            element
        )
        self.driver.execute_script("arguments[0].click();", element)

    def wait_until_url_contains(self, expected_partial_url):
        self.wait.until(
            EC.url_contains(expected_partial_url),
            message=f'Expected "{expected_partial_url}" not in "{self.driver.current_url}"'
        )

    def verify_text(self, expected_text, *locator):
        actual_text = self.find_element(*locator).text
        assert actual_text == expected_text, \
            f'Expected "{expected_text}", but got "{actual_text}"'
