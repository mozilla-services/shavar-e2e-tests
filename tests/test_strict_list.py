import pytest
import time

from pages.strictlist import StrictListPage

@pytest.mark.nondestructive
@pytest.mark.firefox_preferences({'privacy.trackingprotection.enabled': False})
def test_strict_list(base_url, selenium, conf, channel, pref_set):
    """Test Firefox Tracking Protection strict list."""

    page = StrictListPage(selenium, base_url).open()
    page.tracking_protection_always_on()
    time.sleep(3)
    #TODO: figure out how to change blocklist option via setting prefs as the xul elements on about:preferences#privacy are difficult
