import time

from helper_prefs import (
  filesize_index,
  pref_sets_combined_file_lists,
  safebrowsing_files_unique,
  safebrowsing_files_local_expected,
)

def pretty_print(label, list_input):
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    print('=============================================')
    print(label.upper())
    print('=============================================')
    pp.pprint(list_input)


#def test_safebrowsing_contains_expected_files(conf, pref_set, browser, selenium, path_safebrowsing): # noqa
def test_safebrowsing_contains_expected_files(selenium, conf, pref_set, path_safebrowsing): # noqa
    """Hardcoded location of safebrowsing directory will need to be updated
    to reflect new FF profile file directory. Also, hardcoded profile type
    'moztestpub' needs to be updated to reflect test profile type."""

    time.sleep(100)
    selenium.get('about:config')

    #  list of unique local safebrowsing files (no file ext)
    #local = safebrowsing_files_unique(path_profile)
    local = safebrowsing_files_unique(path_safebrowsing)
    expected = pref_sets_combined_file_lists(conf, pref_set)
    pretty_print('local', local)
    pretty_print('expected', expected)
    """
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    print('***********************************')
    print('LOCAL')
    print('***********************************')
    pp.pprint(local)
    print('***********************************')
    print('EXPECTED')
    print('***********************************')
    pp.pprint(expected)
    print('***********************************')
    """
    assert set(expected).issubset(set(local))

"""
#def test_safebrowsing_filesize(conf, pref_set, browser, selenium, path_profile): # noqa
def test_safebrowsing_filesize(conf, pref_set, browser, selenium, path_safebrowsing): # noqa

    # TODO: do we actually need to open the browser to create a
    #       safebrowsing folder?
    selenium.get('about:config')
    time.sleep(30)

    sections_filesizes = filesize_index(conf)
    for section in sections_filesizes:
        print('----------------')
        print(section)
        print('----------------')
        size_threshold = conf.get(section, 'size_threshold')
        threshold_operation = conf.get(section, 'threshold_operation')
        found_expected = safebrowsing_files_local_expected(
            conf, section, path_safebrowsing)

        for f in found_expected:
            conditional = '{0} {1} {2}'.format(
                f[1], threshold_operation, size_threshold)
            #print(f)
            assert eval(conditional), 'Filesize unexpected'
"""
