import os
import sys
import ConfigParser
import pytest

from foxpuppet import FoxPuppet
from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


from helper_prefs import set_prefs # noqa
from firefox_profile import create_mozprofile


    
@pytest.fixture()
def conf():
    config = ConfigParser.ConfigParser()
    config.read('prefs.ini')
    return config

"""
@pytest.fixture
def firefox_binary(firefox_binary):
    return binary('.')
"""

@pytest.fixture
#def firefox_path_profile():
def path_profile():
    f = Firefox()
    return '{0}/safebrowsing'.format(f.capabilities['moz:profile'])

"""
@pytest.fixture()
def path_profile(firefox_path_profile):
    return firefox_path_profile 
"""


@pytest.fixture
#def firefox_options(firefox_options):
#def firefox_options(firefox_options, firefox_path_profile):
def firefox_options(firefox_options, path_profile):
    path_binary = '/Users/rpappalardo/git/ff-tool/.cache/browsers/FirefoxNightly.app/Content/MacOS/firefox-bin'
    c = conf()
    name_section = 'mozstd'
    #path_profile = '/Users/rpappalardo/git/shavar-e2e-tests/.profiles/rpapa2'
    #path_profile = create_mozprofile('rpapa2')
    #path_profile = '/Users/rpappalardo/git/shavar-e2e-tests/.profiles/rpapa2'
    #firefox_options.profile = FirefoxProfile(profile_directory=path_profile)
    #firefox_options.binary = FirefoxBinary(path_binary)
    #firefox_options.profile = path_profile

    f = Firefox()
    path_profile = f.capabilities['moz:profile']
    #path_profile = firefox_path_profile
    firefox_options.set_preference('browser.startup.homepage', "google.com")
    firefox_options.set_preference('privacy.trackingprotection.enabled',True)

    # 1. Set default conf values (loop through them)
    defaults = c.items(name_section)
    for key, val in defaults:
        print(key, val)
    # 2. Set test env (stage or prod)
    # This will come from an environment variable
    # 3. Set "pref_set" values, this will come from an env. variable
    # TASK B
    # 4. Use prefs.ini index to loop through battery of pref lists
    # 5. research a means for re-running tests multiple times, each time with diff env var # noqa
    # (the env var will equal a pref set value, which will also pull from prefs.ini index) # noqa

    # TASK C
    ##firefox_options.binary = <path to binary>
    return firefox_options


@pytest.fixture
def browser(foxpuppet):
    """First Firefox browser window opened."""
    return foxpuppet.browser


@pytest.fixture
def foxpuppet(selenium, firefox_options):
    """Initialize the FoxPuppet object."""
    #driver = webdriver.Firefox(firefox_options=firefox_options)
    return FoxPuppet(selenium)


def pytest_addoption(parser):
    parser.addoption("--pref-set", action="append", default=[],
                     help="prefset to test")


def pytest_generate_tests(metafunc):
    c = conf()
    index = c.get('index', 'pref_sets_index')
    if index:
        index = index.split(',') 

    pref_set = metafunc.config.getoption('pref_set')
    if pref_set:
        metafunc.parametrize('pref_set', pref_set)
    else:
        metafunc.parametrize('pref_set', index)
