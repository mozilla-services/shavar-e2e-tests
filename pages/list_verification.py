from pypom import Page


class ListVerificationPage(Page):

    URL_TEMPLATE = 'https://shavar.stage.mozaws.net/list?client=foo&appver=1&pver=2.2'

    def __init__(self, resp_data):
        self.resp_data = resp_data
        self.headers = {'content-type': 'text/xml; charset=utf-8'}

    def read(self):
        return self.resp_data

# def urlopen(request):
#     return Response(r'<xml document>')
