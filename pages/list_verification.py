from pypom import Page
import urllib2
import requests


class ListVerificationPage(Page):

    URL_TEMPLATE = 'https://shavar.stage.mozaws.net/list?client=foo&appver=1&pver=2.2'

    def read_lists(self):
        url2 = 'https://shavar.stage.mozaws.net/list?client=foo&appver=1&pver=2.2'
        data = requests.get(url2)
        t = str(data.text)
        s = t.split()
        list = sorted(s)
        return list

    def read_list(self, list):
        url3 = 'https://shavar.stage.mozaws.net/downloads?client=foo&appver=1&pver=2.2'
        req = requests.post(url3, data=list)
        return str(req.text).splitlines()
