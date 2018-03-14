import ConfigParser
import os
import shutil
import sys
import time
from foxpuppet import FoxPuppet
import pytest
from selenium.webdriver import Firefox
from helper_prefs import set_prefs # noqa
from os_handler import OSHandler


PATH_CACHE = '.firefox'
TEST_ENV = os.environ['TEST_ENV']


@pytest.fixture()
def conf():
    config = ConfigParser.ConfigParser()
    config.read('prefs.ini')
    return config


@pytest.fixture
def path_safebrowsing(firefox_options):
    path_profile = firefox_options.profile
    path_safebrowsing = '{0}/safebrowsing'.format(path_profile)
    print('PATH_SAFEBROWSING: {0}'.format(path_safebrowsing))
    return path_safebrowsing


def path_profile(pref_set):
    path_profile_dest = '{0}/profiles/{1}'.format(PATH_CACHE, pref_set)
    return path_profile_dest


@pytest.fixture
def profile_copy(driver, pref_set):
    path_profile_dest = path_profile(pref_set)
    path = driver.capabilities['moz:profile']
    try:
        shutil.rmtree(path_profile_dest)
        time.sleep(5)
    except:
        pass
    # TODO: remove this
    time.sleep(30)
    print('\n====================================')
    print('PATH: {0}'.format(path))
    resp = os.listdir('{0}/safebrowsing'.format(path))
    print('\n====================================')
    print(resp)
    time.sleep(10)

    shutil.copytree(path, path_profile_dest)


@pytest.fixture
def browser(foxpuppet):
    """First Firefox browser window opened."""
    return foxpuppet.browser


@pytest.fixture
def foxpuppet(selenium):
    """Initialize the FoxPuppet object."""
    return FoxPuppet(selenium)


@pytest.fixture
def firefox_options(conf, firefox_options, pref_set):
    for section in ['default', TEST_ENV, pref_set]:
        for name, value in conf.items(section):
            firefox_options.set_preference(name, value == 'true' or value)
    return firefox_options


@pytest.fixture
def firefox_path(channel):
    h = OSHandler()
    this_os = h.get_os()

    # remove OSHandler once docker in place
    if this_os == 'mac':
        channel = channel.title()
        path_firefox = '{0}/browsers/Firefox{1}.app/Contents/MacOS/firefox-bin'.format(PATH_CACHE, channel) # noqa
        path_firefox = path_firefox.encode('utf-8')
    elif this_os == 'linux':
        # download must detar to firefox-nightly or firefox-release
        path_firefox = '{0}/browsers/firefox-{1}/firefox-bin'.format(
            PATH_CACHE, channel)
        path_firefox = path_firefox.encode('utf-8')
        pass
    else:
        sys.exit('ERROR: OS not supported')
    return path_firefox


@pytest.fixture
def selenium(pref_set, firefox_options):
    """Start Firefox with custom preferences.
    1. create Firefox object (with custom options)
    2. copy profile to local cache for later use
    3. quit firefox when test completed
    """
    driver = Firefox(firefox_options=firefox_options)
    profile_copy(driver, pref_set)
    yield driver
    driver.quit()


def pytest_addoption(parser):
    parser.addoption("--pref-set", action="append", default=[],
                     help="prefset to test")
    parser.addoption("--channel", action="append", default=[],
                     help="channel to test ['nightly', 'release']")


def pytest_generate_tests(metafunc):
    c = conf()
    if TEST_ENV == 'stage':
        index = c.get('index', 'pref_sets_index_stage')
    else:
        index = c.get('index', 'pref_sets_index_prod')

    if index:
        index = index.split(',')

    pref_set = metafunc.config.getoption('pref_set')
    if pref_set:
        metafunc.parametrize('pref_set', pref_set)
    else:
        metafunc.parametrize('pref_set', index)

    channel = metafunc.config.getoption('channel')
    if channel:
        metafunc.parametrize('channel', channel)
    else:
        metafunc.parametrize('channel', ['nightly', 'release'])
