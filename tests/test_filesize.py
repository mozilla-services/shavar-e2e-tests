import time

from helper_prefs import (
  filesize_index,
  pref_sets_combined_file_lists,
  safebrowsing_files_unique,
  safebrowsing_files_local_expected,
)


def test_safebrowsing_contains_expected_files(conf, pref_set, browser, selenium, path_profile): # noqa
    """Hardcoded location of safebrowsing directory will need to be updated
    to reflect new FF profile file directory. Also, hardcoded profile type
    'moztestpub' needs to be updated to reflect test profile type."""
    print('YOYOYOY: {0}'.format(path_profile))

    selenium.get('about:config')
    time.sleep(5)

    f = safebrowsing_files_unique(path_profile)
    expected = pref_sets_combined_file_lists(conf, pref_set)
    assert set(expected).issubset(set(f))


def test_safebrowsing_filesize(conf, pref_set, browser, selenium, path_profile): # noqa

    # TODO: do we actually need to open the browser to create a
    #       safebrowsing folder?
    selenium.get('about:config')
    time.sleep(3)

    sections_filesizes = filesize_index(conf)
    for section in sections_filesizes:
        print('----------------')
        print(section)
        print('----------------')
        size_threshold = conf.get(section, 'size_threshold')
        threshold_operation = conf.get(section, 'threshold_operation')
        found_expected = safebrowsing_files_local_expected(
            conf, section, path_profile)

        for f in found_expected:
            conditional = '{0} {1} {2}'.format(
                f[1], threshold_operation, size_threshold)
            print(f)
            assert eval(conditional), 'Filesize unexpected'
