import time
import pytest
from helper_prefs import (
  filesize_index,
  pref_sets_combined_file_lists,
  safebrowsing_files_unique,
  safebrowsing_files_local_expected,
)
from conftest import path_safebrowsing_files


def test_safebrowsing_contains_expected_files(selenium, conf, pref_set, channel): # noqa
    """Test compares expected files with what is actually there.
    """

    time.sleep(60)
    safebrowsing_files = path_safebrowsing_files(pref_set)
    f = safebrowsing_files_unique(safebrowsing_files)

    expected = pref_sets_combined_file_lists(conf, pref_set)
    print('----------------------unique--------------------------')
    print(f)
    print('----------------------expected------------------------')
    print(expected)
    print('------------------------------------------------------')
    assert set(expected).issubset(set(f))


@pytest.mark.skip(reason='na')
def test_safebrowsing_filesize(selenium, conf, pref_set, channel): # noqa
    """Verify safebrowsing files are within correct size thresholds.
    """

    time.sleep(10)
    safebrowsing_files = path_safebrowsing_files(pref_set)
    sections_filesizes = filesize_index(conf)

    for section in sections_filesizes:
        size_threshold = conf.get(section, 'size_threshold')
        threshold_operation = conf.get(section, 'threshold_operation')
        found_expected = safebrowsing_files_local_expected(
            conf, section, safebrowsing_files)

        for f in found_expected:
            conditional = '{0} {1} {2}'.format(
                f[1], threshold_operation, size_threshold)
            assert eval(conditional), 'Filesize unexpected'
