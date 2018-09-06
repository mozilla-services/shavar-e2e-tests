import pytest
from selenium.webdriver.support.wait import WebDriverWait
import time


URL_PAGE_BLACKLIST = 'https://washingtonpost.com'
URL_PAGE_WHITELISTED = 'https://www.youtube.com'


@pytest.mark.skip(reason='whatev')
@pytest.mark.firefox_preferences({'privacy.trackingprotection.enabled': True})
def test_tracking_protection_shield_displays(browser, selenium, channel, pref_set):  # noqa
    """Tests if the tracking protection shield icon displays
    on a blacklisted site. (i.e. Washington Post)"""

    selenium.get(URL_PAGE_BLACKLIST)
    WebDriverWait(selenium, timeout=5).until(
        lambda _: browser.navbar.is_tracking_shield_displayed)
    time.sleep(30)
    assert browser.navbar.is_tracking_shield_displayed


@pytest.mark.firefox_preferences({'privacy.trackingprotection.enabled': True})
def test_tracking_protection_shield_does_not_display(browser, selenium, channel, pref_set):  # noqa
    """Tests if the tracking protection shield icon does not display
    on a whitelisted site."""

    selenium.get(URL_PAGE_WHITELISTED)
    time.sleep(900)
    assert not browser.navbar.is_tracking_shield_displayed
