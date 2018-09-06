import json
import pytest
from selenium.webdriver.support.wait import WebDriverWait
from github_handler import (github_repo,
                            json_contents,
                            json_overwrite)
from pages.whitelistedit import WhiteListEditPage


WHITELIST_NAME_ORIG = 'trackwhite.json'
WHITELIST_NAME_NEW = 'trackwhite.json.EDITED'
URL_PAGE_BLACKLIST = 'https://washingtonpost.com'
URL_PAGE_WHITELISTED = 'https://www.youtube.com'


@pytest.fixture(scope='module')
def cache(tmpdir_factory):
    return tmpdir_factory.mktemp('cache').join(WHITELIST_NAME_ORIG)


def setup_whitelist(cache):
    """Save original file contents for restore operation"""

    repo = github_repo()
    message = 'test: setup json for whitelist test'
    contents_orig = json_contents(repo, WHITELIST_NAME_ORIG)
    contents_orig = json.dumps(contents_orig)
    cache.write(contents_orig)

    new_contents = json_contents(repo, WHITELIST_NAME_NEW)
    json_overwrite(repo, WHITELIST_NAME_ORIG, new_contents, message)


def teardown_whitelist(cache):
    """Restore original file contents to github"""

    repo = github_repo()
    message = 'test: revert json for whitelist test'
    contents_orig = cache.read() 
    contents_orig = json.loads(contents_orig)
    json_overwrite(repo, WHITELIST_NAME_ORIG, contents_orig, message)
   

"""Verify in the: Tools > Web Developer > Browser Console, you
should see that doubleclick.net was blocked because of TrackingProtection
"""


@pytest.mark.skip(reason='whatev')
def test_verify_whitelist_in_place(base_url, selenium, conf, channel):
    """Test verifies whitelist not yet changed (items removed) 
    
    NOTE:
        Verify that youtube page does not yet have shield""" 

    page = WhiteListEditPage(selenium, base_url).open()

    # TODO:  need to assert the correct shit here
    assert page.third_party_loads_correctly


@pytest.mark.firefox_preferences({'privacy.trackingprotection.enabled': True})
def test_verify_whitelist_removal(cache, base_url, browser, selenium, conf, channel, pref_set):  # noqa
    """Test verifies behavior with whitelist removal  
    Tests if the tracking protection icon displays
    on a blacklist site.
    
    NOTE:
        Verify that youtube page now has shield""" 

    # TODO:  RESTORE SETUP!!!
    #setup_whitelist(cache)
    
    selenium.get('https://washingtonpost.com')
    WebDriverWait(selenium, timeout=5).until(
        lambda _: browser.navbar.is_tracking_shield_displayed)
    assert browser.navbar.is_tracking_shield_displayed


@pytest.mark.skip(reason='whatev')
def test_verify_whitelist_reverted(cache, base_url, selenium, conf, channel):
    """Test verifies whitelist has been reverted 
    
    NOTE:
        Verify that youtube page no longer has shield""" 

    teardown_whitelist(cache)
    page = WhiteListEditPage(selenium, base_url).open()
    # TODO:  need to assert the correct shit here
    # assert page.third_party_loads_correctly
    assert True
