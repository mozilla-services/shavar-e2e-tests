import pytest
from pages.tp import TrackingProtectionPage


@pytest.mark.nondestructive
def test_tracking_protection_off(base_url, selenium):
    """Test Firefox 'tracking protection' page"""

    page = TrackingProtectionPage(selenium, base_url).open()

    assert page.tracking_protection_off
