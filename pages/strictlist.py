from pypom import Page
from selenium.webdriver.common.by import By


class StrictListPage(Page):

    URL_TEMPLATE = 'about:preferences#privacy'

    _change_block_list_locator = (By.ID, '#changeBlockList')
    _strict_list_locator = 
    _tp_always_on_locator = (By.CSS_SELECTOR, '#trackingProtectionRadioGroup > radio:nth-child(1)')

    def tracking_protection_always_on(self):
        self.find_element(*self._tp_always_on_locator).click()
        self.find_element(*self._change_block_list_locator).click()
