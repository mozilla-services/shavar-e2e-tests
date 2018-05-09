import json
import time
import pytest
from github_handler import (github_repo,
                            json_contents,
                            json_overwrite)
from pages.trackingprotection import TrackingProtectionPage 


BLACKLIST_NAME_ORIG = 'track.json'
BLACKLIST_NAME_NEW = 'track.json.EDITED'


@pytest.fixture(scope='module')
def cache(tmpdir_factory):
    return tmpdir_factory.mktemp('cache').join(BLACKLIST_NAME_ORIG)


def setup_blacklist(cache):
    """Save original file contents for restore operation"""

    repo = github_repo()
    message = 'test: setup json for blacklist test'
    contents_orig = json_contents(repo, BLACKLIST_NAME_ORIG)
    contents_orig = json.dumps(contents_orig)
    cache.write(contents_orig)

    new_contents = json_contents(repo, BLACKLIST_NAME_NEW)
    json_overwrite(repo, BLACKLIST_NAME_ORIG, new_contents, message)


def teardown_blacklist(cache):
    """Restore original file contents to github"""

    repo = github_repo()
    message = 'test: revert json for blacklist test'
    contents_orig = cache.read() 
    contents_orig = json.loads(contents_orig)
    json_overwrite(repo, BLACKLIST_NAME_ORIG, contents_orig, message)
   

def test_verify_no_blacklist(base_url, selenium, conf, channel):
    """Test verifies blacklist not yet set
    
    NOTE:
        A black cat should appear on page"""

    page = TrackingProtectionPage(selenium, base_url).open()

    assert page.tracking_protection_off


def test_verify_blacklist(cache, base_url, selenium, conf, channel):
    """Test verifies blacklist now set
    
    NOTE:
        An orange STOP sign fox should appear on page"""

    setup_blacklist(cache)
    page = TrackingProtectionPage(selenium, base_url).open()
    
    assert page.tracking_protection_on


def test_verify_blacklist_reverted(cache, base_url, selenium, conf, channel):
    """Test verifies blacklist has been reverted 
    
    NOTE:
        A black cat should appear on page"""

    teardown_blacklist(cache)
    page = TrackingProtectionPage(selenium, base_url).open()

    assert page.tracking_protection_off
