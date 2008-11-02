import os
import csv

import dateutil.parser

import econ.data as D
import econ.data.tabular

cache = 'cache'
URL = 'http://www.w3schools.com/browsers/browsers_stats.asp'
retriever = D.Retriever(cache)

class Parser:
    def execute(self):
        self.browsers = []
        self.dates = []
        self.results = {}
        html = retriever.retrieve(URL, force=False)
        reader = econ.data.tabular.HtmlReader()
        tdata = reader.read(html, table_index=2)
        print tdata.data
        self.parse(tdata)
        self.dump()

    def dump(self):
        tdata = econ.data.tabular.TabularData()
        tdata.header = ['Date (Year-Month)'] + self.browsers
        self.dates.sort()
        for dd in self.dates:
            row = [dd] + [ self.results[b].get(dd, '') for b in self.browsers ]
            tdata.data.append(row)
        fileobj = file('data.csv', 'w')
        writer = econ.data.tabular.CsvWriter()
        writer.write(fileobj, tdata)
        fileobj.close()

    def parse(self, tdata):
        self.browsers = set()
        values = {}
        for idx, row in enumerate(tdata.data):
            if idx == 0 or tdata.data[idx-1][0] == '':
                self.browsers.update(set(row[1:]))
        self.browsers = list(self.browsers)
        self.browsers.append('MS (All)')
        self.browsers.append('Opera (All)')
        self.browsers.append('Moz (All)')
        self.browsers.sort()
        for k in self.browsers:
            self.results[k] = {}
        section = []
        for row in tdata.data:
            if row[0] == '':
                self.parse_section(section)
                section = []
            else:
                section.append(row)
        self.parse_section(section)
        # add in extra
        for browser,date_dict in self.results.items():
            for dd,v in date_dict.items():
                if browser.startswith('IE'):
                    self.results['MS (All)'][dd] = \
                            self.results['MS (All)'].get(dd, 0) \
                            + v
                if browser.startswith('N') or browser in ['Fx', 'Moz']:
                    self.results['Moz (All)'][dd] = \
                            self.results['Moz (All)'].get(dd, 0) \
                            + v
                if browser.startswith('O'):
                    self.results['Opera (All)'][dd] = \
                            self.results['Opera (All)'].get(dd, 0) \
                            + v


    def parse_section(self, section):
        year = int(section[0][0])
        for row in section[1:]:
            month = dateutil.parser.parse(row[0]).month
            date = '%d-%02d' % (year, month)
            self.dates.append(date)
            for idx, value in enumerate(row[1:]):
                browser = section[0][idx+1]
                v = value.replace('%', '')
                if v: v = float(v)
                else: v = 0.0
                self.results[browser][date] = v

def test_1():
    p = Parser()
    p.execute()
    assert len(p.browsers) == 20, len(p.browsers)
    ie7 = p.results['IE7']
    assert len(ie7) == 27, len(ie7)
    assert ie7['2008-01'] == 21.2, ie7['2008-01']
    aol = p.results['AOL']
    assert len(aol) == 6, len(aol)
    assert os.path.exists('data.csv')

if __name__ == '__main__':
    p = Parser()
    p.execute()

