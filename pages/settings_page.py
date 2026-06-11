from selenium.webdriver.common.by import By

from pages.base_page import Page


class SettingsPage(Page):
    SETTINGS_OPTION = (
        By.CSS_SELECTOR,
        "a[href*='soft.reelly.io/settings']"
    )
    CONTACT_US_OPTION = (
        By.CSS_SELECTOR,
        "a[href*='/contact-us']"
    )

    def open_settings(self):
        self.wait_until_clickable_click(*self.SETTINGS_OPTION)
        self.wait_until_url_contains('settings')

    def open_contact_us(self):
        self.wait_until_clickable_click(*self.CONTACT_US_OPTION)
