import os

from selenium.webdriver.common.by import By

from pages.base_page import Page


class SignInPage(Page):
    EMAIL_FIELD = (By.CSS_SELECTOR, "input[type='email']")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "input[type='password']")
    LOGIN_BUTTON = (By.XPATH, "//a[normalize-space()='Continue']")
    SETTINGS_LINK = (By.CSS_SELECTOR, "a[href*='soft.reelly.io/settings']")

    def log_in(self):
        email = os.getenv('REELLY_EMAIL')
        password = os.getenv('REELLY_PASSWORD')
        assert email and password, 'Set REELLY_EMAIL and REELLY_PASSWORD before running this test'

        self.wait_until_appear(*self.EMAIL_FIELD)
        self.input_text(email, *self.EMAIL_FIELD)
        self.input_text(password, *self.PASSWORD_FIELD)
        self.wait_until_clickable_click(*self.LOGIN_BUTTON)
        self.wait_until_clickable(*self.SETTINGS_LINK)
