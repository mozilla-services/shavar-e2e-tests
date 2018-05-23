import os
from pypom import Page
import pytest
import urllib2
import requests


TEST_ENV = os.environ['TEST_ENV']


class ListVerificationPage(Page):

    def read_lists(self, conf):
        url = conf.get(TEST_ENV, 'browser.safebrowsing.provider.mozilla.updateURL')
        data = requests.get(url)
        t = str(data.text)
        s = t.split()
        list = sorted(s)
        return list
