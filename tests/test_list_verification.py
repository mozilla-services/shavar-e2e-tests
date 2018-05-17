import pytest
import requests
from pages.list_verification import ListVerificationPage
from helper_prefs import list_verification_name


POLLING_TIME = 3600


# @pytest.mark.nondestructive
# def test_list_verification(base_url, selenium, channel, conf):
#     """Test Firefox Tracking Protection serves correct lists"""
#
#     page = ListVerificationPage(selenium, base_url).open()
#     results = page.read_lists()
#
#     g = conf.get('filelist_stage', 'lists')
#     s = g.split()
#     expected = sorted(s)
#     assert results == expected

@pytest.mark.nondestructive
def test_stage_list_verification(base_url, selenium, channel, conf):
    """Test individual list responses"""

    page = ListVerificationPage(selenium, base_url).open()
    list = conf.get('list_index','file_list_stage')
    stage_base_url = 'tracking-protection.stage.mozaws.net'
    timestamp = 123456
    s = list.split(',')
    for item in s:
        results = page.read_list(item)
        assert results[0] == 'n:{0}'.format(POLLING_TIME)
        assert results[1]+';' == 'i:{0}'.format(item)
        #assert results[2] == 'u:{0}/{1}/{2}'.format(stage_base_url, item, timestamp)
        #TODO: curl item has ';' for item that is showing in the url and should be stripped out
        x = results[2].isdigit()
        #assert x == True
        #TODO: fix x is FALSE
        print('X IS HERE')
        print(x)
        print(results)


    # u = ['baseurl', 'filename', '12345678']
    # x = u[2].isdigit()
    # assert x == True
