import ConfigParser
import os
import shutil
import sys
import time
from foxpuppet import FoxPuppet
import pytest
from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
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


def path_firefox(channel='nightly'):
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


def firefox_binary(channel):
    path_binary = path_firefox(channel)
    return FirefoxBinary(path_binary)


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


def set_preferences(profile, name_section):
    c = conf()
    defaults = c.items(name_section)

    print('\n====================================')
    print('PREF_SET SECTION: {0}'.format(name_section))
    print('====================================\n')

    for key, val in defaults:
        if val == 'true':
            val = True
        profile.set_preference(key, val)
        print('KEY: {0}, VAL: {1}'.format(key, val))
    return profile


def firefox_profile(pref_set):
    profile = FirefoxProfile()
    # 1. Set default values
    profile = set_preferences(profile, 'default')
    # 2. Set test env (stage or prod)
    profile = set_preferences(profile, TEST_ENV)
    # This will come from: see - pytest_generate_tests
    profile = set_preferences(profile, pref_set)
    return profile


@pytest.fixture
def browser(foxpuppet):
    """First Firefox browser window opened."""
    return foxpuppet.browser


@pytest.fixture
def foxpuppet(selenium):
    """Initialize the FoxPuppet object."""
    return FoxPuppet(selenium)


@pytest.fixture
def selenium_setup(pref_set, channel):
    """Setup custom prefs and restart.
    1. create FirefoxBinary object (with custom path)
    2. create FirefoxProfile object (with custom prefs)
    3. create Firefox object (with custom: binary, profile objects)
    4. copy profile to local cache for later use
    5. quit firefox
    """

    binary = firefox_binary(channel)
    profile = firefox_profile(pref_set)

    driver = Firefox(firefox_binary=binary, firefox_profile=profile)
    profile_copy(driver, pref_set)
    driver.quit()


@pytest.fixture
def selenium(pref_set, channel):
    """Start Firefox with custom profile & binary.
    1. create FirefoxBinary object (with custom path)
    2. create FirefoxProfile object (with pre-existing profile
       from selenium_setup)
    3. create Firefox object (with custom: binary, profile objects)
    4. start browser for test
    5. quite firefox when test completed
    """

    path_prof = path_profile(pref_set)

    binary = firefox_binary(channel)
    profile = FirefoxProfile(path_prof)

    driver = Firefox(firefox_binary=binary, firefox_profile=profile)
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
