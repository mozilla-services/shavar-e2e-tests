import time


def test_new(browser, selenium, pref_set):
#def test_new(browser, pref_set):

    """Tests if the tracking protection icon displays"""
    print('PREFSETS: {0}'.format(pref_set))
    time.sleep(300)
    #selenium.get('about:config')
