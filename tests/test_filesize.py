# TO DO: remove hardcoded safebrowsing folder location
# TO DO: Find a way to cycle through these tests using different
# profile types, remove hardcoded line 31
# TO DO: remove extra print statements line 40
# 1. get list of files from local /safebrowsing
# 2. confirm they match expected files
# 3. get filesizes
# 4. get filesize group [ex: whitelist], compare to local matching files
# 5. verify size is under maximum
import os
import time

from helper_prefs import (
  filesize_index,
  pref_sets_combined_file_lists,
  safebrowsing_files_unique,
  safebrowsing_files_local_expected,
)


#def test_safebrowsing_contains_expected_files(conf, pref_set):
#def test_safebrowsing_contains_expected_files(conf, pref_set, browser, selenium)
def test_safebrowsing_contains_expected_files(conf, pref_set, browser, selenium, path_profile):
    """Hardcoded location of safebrowsing directory will need to be updated
    to reflect new FF profile file directory. Also, hardcoded profile type
    'moztestpub' needs to be updated to reflect test profile type."""
    print('YOYOYOY: {0}'.format(path_profile))

    selenium.get('about:config')
    time.sleep(3)

    #f = safebrowsing_files_unique()
    f = safebrowsing_files_unique(path_profile)
    expected = pref_sets_combined_file_lists(conf, pref_set)
    assert set(expected).issubset(set(f))


#def test_safebrowsing_filesize(conf, pref_set):
#def test_safebrowsing_filesize(conf, pref_set, browser, selenium):
def test_safebrowsing_filesize(conf, pref_set, browser, selenium, path_profile):

    selenium.get('about:config')
    time.sleep(3)

    sections_filesizes = filesize_index(conf)
    for section in sections_filesizes:
        print('----------------')
        print(section)
        print('----------------')
        size_threshold = conf.get(section, 'size_threshold')
        threshold_operation = conf.get(section, 'threshold_operation')

        #found_expected = safebrowsing_files_local_expected(conf, section)
        found_expected = safebrowsing_files_local_expected(conf, section, path_profile)

        for f in found_expected:
            conditional = '{0} {1} {2}'.format(
                f[1], threshold_operation, size_threshold)
            print(f)
            assert eval(conditional), 'Filesize unexpected'
