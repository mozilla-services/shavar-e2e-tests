import ConfigParser
import pytest
from foxpuppet import FoxPuppet
from selenium.webdriver import Firefox


from helper_prefs import set_prefs # noqa


@pytest.fixture()
def conf():
    config = ConfigParser.ConfigParser()
    config.read('prefs.ini')
    return config


"""
@pytest.fixture
#def path_profile(foxpuppet, pref_set):
#def path_profile(capabilities, pref_set):
def path_profile(selenium, pref_set):
    #f = foxpuppet.selenium
    #path = f.capabilities['moz:profile']
    path = capabilities['moz:profile']

    # copy profile to .profile
    path_profile_dest = '.profiles/{0}'.format(pref_set)
    import shutil
    shutil.copytree(path, path_profile_dest)


    #path = '{0}/safebrowsing'.format(f.capabilities['moz:profile'])
    #path_safebrowsing = '{0}/safebrowsing'.format(path)
    #path_safebrowsing = '{0}/safebrowsing'.format(path_profile_dest)
    #print('PATH_SAFEBROWSING (PATH_PROFILE): {0}'.format(path_safebrowsing))
    #return path_safebrowsing
    return path_profile_dest
"""


@pytest.fixture
#def path_safebrowsing(path_profile):
def path_safebrowsing(firefox_options):
    path_profile = firefox_options.profile
    path_safebrowsing = '{0}/safebrowsing'.format(path_profile)
    print('PATH_SAFEBROWSING (PATH_PROFILE): {0}'.format(path_safebrowsing))
    return path_safebrowsing


    return
def set_preferences(firefox_options, name_section):
    c = conf()
    defaults = c.items(name_section)
    print('\n====================================')
    print('PREF_SET SECTION: {0}'.format(name_section))
    print('====================================\n')
    for key, val in defaults:
        if val == 'true':
            val = True
        firefox_options.set_preference(key, val)
        print('KEY: {0}, VAL: {1}'.format(key, val))
    return firefox_options



@pytest.fixture
def capabilities(capabilities):
    capabilities['firefox_binary'] = '/Users/rpappalardo/git/ff-tool/.cache/browsers/FirefoxNightly.app/Contents/MacOS/firefox-bin' # noqa
    return capabilities


@pytest.fixture
#def firefox_options(firefox_options, pref_set):
#def firefox_options(firefox_options, pref_set, path_profile):
#def firefox_options(firefox_options, capabilities, pref_set): #, path_profile):
#def firefox_options(firefox_options, selenium, pref_set): #, path_profile):
#def firefox_options(firefox_options, pref_set, path_profile):
def firefox_options(firefox_options, pref_set):

    # TODO: open browser to restart and hit shavar
    # https://github.com/mozilla/FoxPuppet/blob/e01c7dd8e1f94d28b64caf67420f53c836432777/docs/user_guide.rst

    # SET PREFS
    # 1. Set default conf values (loop through them)
    firefox_options = set_preferences(firefox_options, 'default')
    # 2. Set test env (stage or prod)
    firefox_options = set_preferences(firefox_options, 'stage')
    # This will come from: see - pytest_generate_tests
    firefox_options = set_preferences(firefox_options, pref_set)


    # SET BINARY
    # path_binary = '/Users/rpappalardo/git/ff-tool/.cache/browsers/FirefoxNightly.app/Contents/MacOS/firefox-bin' # noqa
    #firefox_options.binary = '/Users/rpappalardo/git/ff-tool/.cache/browsers/FirefoxNightly.app/Contents/MacOS/firefox-bin'.encode('utf-8') # noqa
    #firefox_options.binary = str('/Users/rpappalardo/git/ff-tool/.cache/browsers/FirefoxNightly.app/Contents/MacOS/firefox-bin') # noqa

    # launch browser
    # quit browser
    #path_profile = selenium.capabilities['moz:profile']
    #firefox_options.profile = path_profile 
    #print('FIREFOX_OPTIONS_CAPS: {0}'.format(firefox_options.to_capabilities()))
    #print('FIREFOX_OPTIONS_PROFILE: {0}'.format(firefox_options.profile))
    #return firefox_options


    # SET PROFILE
    #path = firefox_options.profile

    """
    path = capabilities['moz:profile']

    # copy profile to .profile
    path_profile_dest = '.profiles/{0}'.format(pref_set)
    import shutil
    print('PATH:{0} ---- DEST: {1}'.format(path, path_profile_dest))
    shutil.copytree(path, path_profile_dest)
    firefox_options.profile = path_profile_dest 
    path = capabilities['moz:profile']
    """

    return firefox_options


@pytest.fixture
def browser(foxpuppet):
    """First Firefox browser window opened."""
    return foxpuppet.browser

"""
@pytest.fixture
def selenium(selenium):
    #path = '{0}/safebrowsing'.format(selenium.capabilities['moz:profile'])
    #print('PATH_SAFEBROWSING (SELENIUM FIXTURE): {0}'.format(path))
    return selenium
"""

@pytest.fixture
def foxpuppet(selenium):
    """Initialize the FoxPuppet object."""
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
