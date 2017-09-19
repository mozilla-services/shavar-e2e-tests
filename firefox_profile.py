import os
from tempfile import mkdtemp
#from mozprofile import FirefoxProfile as FFProfile, Preferences
from selenium.webdriver import FirefoxProfile
from mozprofile import FirefoxProfile as FFProfile
from mozprofile import Preferences

"""
from selenium.webdriver import Firefox
f = Firefox()
print(f.capabilities['moz:profile'])
#'/var/folders/wz/3v_j7g2n2zx_q6qs8g7vmyg00000gn/T/rust_mozprofile.GHzHQe690rQE'
path_profile = f.capabilities['moz:profile']
print('{0}/safebrowsing'.format(path_profile))
"""

BASE_PROFILE_DIR = '.profiles'


def create_mozprofile(profile_dir):
    print('PROFILE_DIR: {0}'.format(profile_dir))

    profile_dir = 'rpapa2'
    if not os.path.exists(BASE_PROFILE_DIR):
        os.mkdir(BASE_PROFILE_DIR)

    if not profile_dir:
        full_profile_dir = mkdtemp(
            dir=BASE_PROFILE_DIR,
            prefix="pref-set.",
            suffix=""
        )

    else:
        full_profile_dir = os.path.join(BASE_PROFILE_DIR, profile_dir)

    prefs = Preferences()

    # Add custom user pref: `fftool.profile.name`
    prefs.add([("profile.name", full_profile_dir)])

    #profile = FirefoxProfile(
    profile = FFProfile(
        profile=full_profile_dir,
        restore=False,
        preferences=prefs())

    return full_profile_dir
