import time


def test_new(browser, selenium, pref_set):
    """Tests if the tracking protection icon displays"""
    print('PREFSETS: {0}'.format(pref_set))
    selenium.get('about:config')
    time.sleep(30)
