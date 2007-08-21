# Download and manipulate data from Millenium Development Goals Project
# http://mdgs.un.org/unsd/mdg/
import urllib
import zipfile
from StringIO import StringIO

def download_data(series_id, format='csv'):
    """Download a given data series.

    @format: csv, xml, xls (excel)
    """
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

def parse_data_file(csv_fo):
    pass

class MdgMetadata(object):

    def __init__(self):
        metadata_csv = self._load_cached_metadata()
        self.series = self._parse_metadata_csv(metadata_csv)

    def _load_cached_metadata(self):
        import pkg_resources
        metafo = pkg_resources.resource_stream('econ.mdg', 'mdg_metadata.txt')
        return metafo

    def _parse_metadata_csv(self, fileobj):
        outdict = {}
        import csv
        reader = csv.reader(fileobj)
        for row in reader:
            series_id = int(row[0])
            title = row[1]
            outdict[series_id] = title
        return outdict

    def _download_metadata():
        # does *NOT* work because of nasty javascript
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

                
if __name__ == '__main__':
    out = download_data(580, 'csv')
    print out

