import pytest
from selenium.webdriver.support.wait import WebDriverWait


@pytest.mark.firefox_preferences({'privacy.trackingprotection.enabled': True})
def test_tracking_protection_shield_displays(browser, selenium, channel, pref_set):
    """Tests if the tracking protection icon displays on a blacklist site."""
    selenium.get('https://www.washingtonpost.com/')
    WebDriverWait(selenium, timeout=5).until(
        lambda _: browser.navbar.is_tracking_shield_displayed)
    assert browser.navbar.is_tracking_shield_displayed

@pytest.mark.firefox_preferences({'privacy.trackingprotection.enabled': True})
def test_tracking_protection_shield_does_not_display(browser, selenium, channel, pref_set):
    """Tests if the tracking protection icon does not display on a whitelist site."""
    selenium.get('https://www.youtube.com/')
    assert not browser.navbar.is_tracking_shield_displayed
