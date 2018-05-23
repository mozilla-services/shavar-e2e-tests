import os
import pytest
import requests
import time
from pages.list_verification import ListVerificationPage


CLIENT_CHECK_DELAY = 3600
TEST_ENV = os.environ['TEST_ENV']


@pytest.mark.nondestructive
def test_list_verification(base_url, selenium, channel, conf):
    """Test Firefox Tracking Protection serves correct lists"""
    base_url = conf.get(TEST_ENV, 'browser.safebrowsing.provider.mozilla.updateURL')
    page = ListVerificationPage(selenium, base_url).open()
    results = page.read_lists(conf)

    g = conf.get('filelist_{0}'.format(TEST_ENV), 'lists')
    s = g.split()
    expected = sorted(s)
    assert results == expected

@pytest.mark.nondestructive
def test_individual_list_verification(base_url, selenium, channel, conf):
    """Test individual list responses"""
    update_url = conf.get(TEST_ENV, 'browser.safebrowsing.provider.mozilla.downloads')
    page = ListVerificationPage(selenium, base_url).open()
    list = conf.get('list_index','file_list_{0}'.format(TEST_ENV))
    s = list.split(',')
    for item in s:
        results = page.read_individual_list(conf, item)
        assert results[0] == 'n:{0}'.format(CLIENT_CHECK_DELAY)
        assert results[1]+';' == 'i:{0}'.format(item)
        t = results[2].split('/')
        assert t[0] == 'u:{0}'.format(conf.get(TEST_ENV, 'base_domain'))
        assert t[1]+';' == item
        assert t[2].isdigit()
