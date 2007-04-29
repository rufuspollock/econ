# Download and manipulate data from Millenium Development Goals Project
# http://mdgs.un.org/unsd/mdg/
import urllib
import zipfile
from StringIO import StringIO

def download_data(series_id, format='csv'):
    # format = Csv always
    format = format.capitalize()
    url = 'http://mdgs.un.org/unsd/mdg/Handlers/ExportHandler.ashx' + \
            '?Type=%s&Series=%s' % (format, series_id)
    openurl = urllib.urlopen(url)
    tfo = StringIO(openurl.read())
    zipfo = zipfile.ZipFile(tfo)
    # there is just one item in the zip archive
    name = zipfo.namelist()[0]
    out = zipfo.read(name)
    return out

def parse_mdg_csv(csv):
    pass


def grab_metadata():
    # does *not* work because of nasty javascript
    # probably need to use selenium
    from mechanize import Browser
    br = Browser()
    br.addheaders = [ ('User-agent', 'Firefox') ]
    br.set_handle_robots(False)
    br.open('http://mdgs.un.org/unsd/mdg/Metadata.aspx')
    br.follow_link(text='Flat View')
    assert br.viewing_html()
    out = br.response().read()
    # TODO: extract option list and then clean up
    return out

class TestStuff:

    def test_1(self):
        # series 580: Population below $1 (PPP) per day consumption,
        # percentage
        out = download_data(580)
        assert len(out) > 0
        print out[:30]

    def test_grab_metadata(self):
        # out = grab_metadata()
        # print out
        # assert len(out) == 0
        pass

                
if __name__ == '__main__':
    out = download_data(580, 'csv')
    print out

