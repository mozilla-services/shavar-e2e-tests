import pytest
from pages.trackingprotection import TrackingProtectionPage
from conftest import firefox_download


@pytest.mark.nondestructive
def test_tracking_protection_off(base_url, selenium):
    """Test Firefox Tracking Protection page shows TP is off"""

    firefox_download()
    page = TrackingProtectionPage(selenium, base_url).open()

    assert page.tracking_protection_off


@pytest.mark.nondestructive
def test_tracking_protection_on(base_url, selenium):
    """Test Firefox Tracking Protection page shows TP is on"""
    # This test will fail until we have profile integration

    firefox_download()
    page = TrackingProtectionPage(selenium, base_url).open()

    assert page.tracking_protection_on
