import time
import pytest

from helper_prefs import (
  filesize_index,
  pref_sets_combined_file_lists,
  safebrowsing_files_unique,
  safebrowsing_files_local_expected,
)
from conftest import path_profile, PATH_CACHE


def test_safebrowsing_contains_expected_files(selenium, conf, pref_set, channel): # noqa
#def test_safebrowsing_contains_expected_files(selenium, conf, pref_set, channel): # noqa
    """Hardcoded location of safebrowsing directory will need to be updated
    to reflect new FF profile file directory. Also, hardcoded profile type
    'moztestpub' needs to be updated to reflect test profile type."""

    selenium.get('about:config')
    time.sleep(50)

    path_prof = path_profile(pref_set)
    f = safebrowsing_files_unique(path_prof)
    expected = pref_sets_combined_file_lists(conf, pref_set)
    assert set(expected).issubset(set(f))

"""
def test_safebrowsing_filesize(selenium_setup, selenium, conf, pref_set, channel): # noqa

    selenium.get('about:config')
    time.sleep(3)

    path_prof = path_profile(pref_set)
    sections_filesizes = filesize_index(conf)
    for section in sections_filesizes:
        print('----------------')
        print(section)
        print('----------------')
        size_threshold = conf.get(section, 'size_threshold')
        threshold_operation = conf.get(section, 'threshold_operation')
        found_expected = safebrowsing_files_local_expected(
            conf, section, path_prof)

        for f in found_expected:
            conditional = '{0} {1} {2}'.format(
                f[1], threshold_operation, size_threshold)
            assert eval(conditional), 'Filesize unexpected'
"""
