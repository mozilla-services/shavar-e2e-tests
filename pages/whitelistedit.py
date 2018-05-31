from pypom import Page
from selenium.webdriver.common.by import By


class WhiteListEditPage(Page):

    URL_TEMPLATE = 'https://www.youtube.com'

    _dnt_signal_locator = (By.ID, 'dnt-on')
    _first_party_locator = (By.ID, 'whitelisted-loaded')
    _third_party_locator = (By.ID, 'blacklisted-blocked')

    """Verify in the: Tools > Web Developer > Browser Console, you should
    see that doubleclick.net was blocked because of TrackingProtection
    """
    @property
    def third_party_loads_correctly(self):
        return self.is_element_displayed(*self._third_party_locator)

    @property
    def first_party_loads_correctly(self):
        return self.is_element_displayed(*self._first_party_locator)

    @property
    def dnt_signal_correctly_sent(self):
        return self.is_element_displayed(*self._dnt_signal_locator)
