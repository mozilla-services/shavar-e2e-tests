import pytest
from pages.list_verification import ListVerificationPage


@pytest.mark.nondestructive
def test_list_verification(base_url, selenium, channel):
    page = ListVerificationPage(selenium, base_url).open()
    print(page.read)
    print('print statement')

# def test_list_verification(browser, selenium, channel, pref_set):
#     """Tests if the tracking protection icon does not display on a whitelist site."""
#     selenium.get('https://shavar.stage.mozaws.net/list?client=foo&appver=1&pver=2.2')
#     assert not browser.navbar.is_tracking_shield_displayed
