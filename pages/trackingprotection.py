from pypom import Page
from selenium.webdriver.common.by import By


class TrackingProtectionPage(Page):

    URL_TEMPLATE = 'https://mozilla.github.io/tracking-test/'

    _cat_locator = (By.CSS_SELECTOR, '#cat')
    _fox_locator = (By.CSS_SELECTOR, '#fox')

    @property
    def tracking_protection_off(self):
        return self.is_element_displayed(*self._cat_locator)

    @property
    def tracking_protection_on(self):
        return self.is_element_displayed(*self._fox_locator)
