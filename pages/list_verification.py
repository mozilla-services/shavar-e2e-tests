import os
from pypom import Page
import pytest
import urllib2
import requests


TEST_ENV = os.environ['TEST_ENV']


class ListVerificationPage(Page):

    URL_TEMPLATE = 'https://shavar.stage.mozaws.net/list?client=foo&appver=1&pver=2.2'

    def read_lists(self, conf):
        url = conf.get(TEST_ENV, 'browser.safebrowsing.provider.mozilla.updateURL')
        data = requests.get(url)
        t = str(data.text)
        s = t.split()
        list = sorted(s)
        return list

    def read_individual_list(self, conf, list):
        url = conf.get(TEST_ENV, 'browser.safebrowsing.provider.mozilla.downloads')
        req = requests.post(url, data=list)
        return str(req.text).splitlines()
