from selenium.webdriver.common.by import By

from pages.base_page import Page


class ContactUsPage(Page):
    CONTACT_US_TITLE = (
        By.XPATH,
        "//*[contains(normalize-space(), 'Join us in social media')]"
    )
    SOCIAL_MEDIA_ICONS = (
        By.CSS_SELECTOR,
        "a[href*='instagram'], a[href*='t.me/reellydxb'], "
        "a[href*='youtube'], a[href*='linkedin']"
    )
    CONNECT_COMPANY_BUTTON = (
        By.XPATH,
        "//a[contains(normalize-space(), 'Connect the company')]"
    )

    def verify_contact_us_page_opened(self):
        self.wait_until_url_contains('contact')
        self.wait_until_visible(*self.CONTACT_US_TITLE)

    def verify_at_least_four_social_media_icons(self):
        icons = self.find_elements(*self.SOCIAL_MEDIA_ICONS)
        assert len(icons) >= 4, f'Expected at least 4 social media icons, but got {len(icons)}'

    def verify_connect_company_button_clickable(self):
        self.wait_until_clickable(*self.CONNECT_COMPANY_BUTTON)
