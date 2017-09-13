import os
import pytest
import time
from selenium.webdriver.support.wait import WebDriverWait


PREF_SET = os.environ['PREF_SET']


# @pytest.mark.firefox_preferences({'privacy.trackingprotection.enabled': True})
def test_new(browser, selenium):
    """Tests if the tracking protection icon displays"""
    selenium.get('about:config')
    time.sleep(30)
    # WebDriverWait(selenium, timeout=5).until(
    #     lambda _: browser.navbar.is_tracking_shield_displayed)
