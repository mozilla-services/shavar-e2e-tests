import os
import json
from selenium import webdriver


PATH_DIR = './safebrowsing'


dir = ('safebrowsing')
sections = ['whitelist', 'blacklist', 'content', 'DNT', 'plugin']


def filesize_index(conf):
    return conf.get('index', 'filesize_index').split(',')


def max_file_size_file_list(conf, name_section):
    # returns expected "max file size" grouping file_list from prefs.ini
    return conf.get(name_section, 'file_list').split(',')


def pref_sets_combined_file_lists(conf, section_name):
    items = conf.items(section_name)
    file_list = []
    for (key, val) in items:
        list_tmp = val.split(',')
        for item in list_tmp:
            file_list.append(item)
    return file_list


def pref_sets_index(conf):
    return conf.get('index', 'pref_sets_index').split(',')


def safebrowsing_files_local():
    found = []
    for filename in os.listdir(PATH_DIR):
        file_path = '{0}/{1}'.format(PATH_DIR, filename)
        fsize = os.path.getsize(file_path)
        tmp = (filename, fsize)
        found.append(tmp)
    return found


def safebrowsing_files_local_expected(conf, section):
    found = safebrowsing_files_local()
    expected = set(max_file_size_file_list(conf, section))
    filenames_expected = subset_safebrowsing_prefs(conf, section)
    found_expected = []
    for filename_local in found:
        for filename_expected in filenames_expected:
            if filename_expected == filename_local[0]:
                found_expected.append(filename_local)
    return found_expected


def safebrowsing_files_unique():
    # return list of unique safebrowsing files (less file extension)
    f = []
    for name in os.listdir('safebrowsing'):
        file = os.path.splitext(name)[0]
        if file not in (f):
            f.append(file)
    return f


def sections_list_all(conf):
    # list all sections (prefs.ini)
    return conf.sections()


def section_list_all(conf, name_section):
    # list all items in a given section (prefs.ini)
    return conf.items(name_section)


def set_prefs(conf, sections):
    fp = webdriver.FirefoxProfile()
    for section in sections:
        items = conf.items(section)
        for (key, val) in items:
            fp.set_preference(key, val)
    return fp


def subset_safebrowsing_prefs(conf, section):
    f = []
    expected = set(max_file_size_file_list(conf, section))
    exts = ['pset', 'sbstore']
    filenames_expected = []
    for item in expected:
        for ext in exts:
            filenames_expected.append('{0}.{1}'.format(item, ext))
    return filenames_expected


if __name__ == '__main__':
    import ConfigParser

    def conf():
        config = ConfigParser.ConfigParser()
        config.read('./prefs.ini')
        return config
        conf = conf()

    #val = sections_list_all(conf)
    #val = section_list_all(conf, 'DNT')
    #val = pref_set_file_list(conf, 'DNT')
    #val = pref_sets_list_all(conf)
    #val = max_file_size_list_all(conf)
    #val = max_file_size_file_list(conf, 'whitelist')
    #val = pref_sets_index(conf)
    #val = pref_sets_combined_file_lists(conf, 'mozfull')
    #print(val)
