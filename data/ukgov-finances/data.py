import os
import re
import urllib

from econ.data import Retriever

import BeautifulSoup as bs

cache = os.path.abspath('./cache')
baseurl = 'http://www.hm-treasury.gov.uk'
url = 'http://www.hm-treasury.gov.uk/pespub_pesa08.htm'
retriever = Retriever(cache)

xls_urls = []

def retrieve():
    doc = retriever.retrieve(url).read()
    soup = bs.BeautifulSoup(doc)

    # find all csv
    for href in soup.findAll('a', href=re.compile('.*\.csv')):
        # print href
        pass

    # find all xls
    for href in soup.findAll('a', href=re.compile('.*\.xls')):
        durl = baseurl + href['href']
        # print 'Retrieving %s' % durl
        xls_urls.append(durl)
        retriever.retrieve(durl)

retrieve()

import econ.data.tabular as T
class Analyzer():

    def extract_simple(self):
        fp = retriever.filepath(xls_urls[0])
        r = T.XlsReader()
        sheet_index = 2
        td = r.read(open(fp), sheet_index)
        cells = td.data
        title = cells[0][0]
        entries = {}
        for row in cells[6:]:
            if row[1]: # not a subheading
                entries[row[0]] = row[1:10]
        years = range(2002, 2011)
        return entries, years
    
    def extract_dept_spend(self):
        fp = retriever.filepath(xls_urls[4])
        r = T.XlsReader()
        sheet_index = 1
        td = r.read(open(fp), sheet_index)
        cells = td.data
        title = cells[0][0]
        # delete last row and column as totals
        headings = cells[3][1:-1] 
        for row in cells[4:-1]:
            data[row[0]] = row[1:-1]

    def crude_totals(self):
        entries, years = self.extract_simple()
        expenditure = entries['Public sector current expenditure']
        import pylab
        pylab.plot(years, expenditure)
        pylab.xlim(xmin=2000)
        pylab.savefig('expenditure.png')

    def dept_spend(self):
        out = self.extract_dept_spend()

if __name__ == '__main__':
    a = Analyzer()
    # a.crude_totals()
    a.dept_spend()

