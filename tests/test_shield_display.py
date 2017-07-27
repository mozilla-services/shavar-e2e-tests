# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import time
from selenium.webdriver.support.wait import WebDriverWait


@pytest.mark.firefox_preferences({'privacy.trackingprotection.enabled': True})
def test_tracking_protection_shield_displays(foxpuppet, selenium):
    """Tests if the tracking protection icon displays"""
    browser = foxpuppet.browser
    assert not browser.navbar.is_tracking_shield_displayed
    selenium.get('https://www.washingtonpost.com/')
    WebDriverWait(selenium, timeout=5).until(
        lambda _: browser.navbar.is_tracking_shield_displayed)


@pytest.mark.firefox_preferences({'privacy.trackingprotection.enabled': True})
def test_tracking_protection_shield_does_not_display(foxpuppet, selenium):
    """Tests if the tracking protection icon does not display"""
    browser = foxpuppet.browser
    assert not browser.navbar.is_tracking_shield_displayed
    selenium.get('https://www.youtube.com/')
    time.sleep(5)
    assert not browser.navbar.is_tracking_shield_displayed
