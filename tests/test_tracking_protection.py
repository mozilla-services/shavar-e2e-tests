import time 
import pytest
from pages.trackingprotection import TrackingProtectionPage


@pytest.mark.nondestructive
@pytest.mark.firefox_preferences({'privacy.trackingprotection.enabled': False})
def test_tracking_protection_off(base_url, selenium, conf, channel, pref_set):
    """Test Firefox Tracking Protection page shows TP is off."""

    page = TrackingProtectionPage(selenium, base_url).open()
    assert page.tracking_protection_off


@pytest.mark.nondestructive
@pytest.mark.firefox_preferences({'privacy.trackingprotection.enabled': True})
def test_tracking_protection_on(base_url, selenium, channel, pref_set):
    """Test Firefox Tracking Protection page shows TP is on."""

    page = TrackingProtectionPage(selenium, base_url).open()
    assert page.tracking_protection_on
