import os
import ConfigParser
import pytest

from foxpuppet import FoxPuppet
from helper_prefs import set_prefs


PREF_SET = os.environ['PREF_SET']


@pytest.fixture()
def conf():
    config = ConfigParser.ConfigParser()
    config.read('prefs.ini')
    return config


@pytest.fixture
# def firefox_options(firefox_options):
def firefox_options(firefox_options):
    name_section = 'mozstd'
    c = conf()
    # TASK A
    firefox_options.set_preference('browser.startup.homepage', "google.com")
    # 1. Set default conf values (loop through them)
    defaults = c.items(name_section)
    for key, val in defaults:
        print(key, val)
    # 2. Set test env (stage or prod)
    # This will come from an environment variable
    # 3. Set "pref_set" values, this will come from an env. variable
    # TASK B
    # 4. Use prefs.ini index to loop through battery of pref lists
    # 5. research a means for re-running tests multiple times, each time with diff env var
    # (the env var will equal a pref set value, which will also pull from prefs.ini index)
    return firefox_options


@pytest.fixture
def browser(foxpuppet):
    """First Firefox browser window opened."""
    return foxpuppet.browser


@pytest.fixture
def foxpuppet(selenium):
    """Initialize the FoxPuppet object."""
    return FoxPuppet(selenium)


def pytest_generate_tests(metafunc):
    metafunc.parametrize('win_size', [(1000,1020), (xx, xx )])
