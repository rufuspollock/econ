import os
import re
import urllib

import BeautifulSoup as bs
import simplejson as sj

from econ.data import Retriever

cache = os.path.join(os.path.dirname(__file__), 'cache')
baseurl = 'http://www.hm-treasury.gov.uk'
url = 'http://www.hm-treasury.gov.uk/pespub_pesa08.htm'
retriever = Retriever(cache)
infopath = os.path.join(cache, 'info.js')


def retrieve():
    xls_urls = []
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
    sj.dump(xls_urls, open(infopath, 'w'))

import econ.data.tabular as T
import pylab
class Analyzer():
    def __init__(self):
        self.xls_urls = sj.load(open(infopath))

    def extract_simple(self):
        fp = retriever.filepath(self.xls_urls[0])
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
        fp = retriever.filepath(self.xls_urls[4])
        r = T.XlsReader()
        sheet_index = 1
        td = r.read(open(fp), sheet_index)
        cells = td.data
        title = cells[0][0]
        # delete last row and column as totals
        headings = cells[3][1:-1] 
        data = {}
        for row in cells[4:-1]:
            data[row[0]] = row[-1]
            # TODO: could do by function and dept
        return data

    def crude_totals(self):
        entries, years = self.extract_simple()
        expenditure = entries['Public sector current expenditure']
        pylab.plot(years, expenditure)
        pylab.xlim(xmin=2000)
        pylab.savefig('expenditure.png')

    def dept_spend(self):
        out = self.extract_dept_spend()
        # delete very small items 
        for k in out.keys():
            if out[k] < 2000: # anything less than 2 billion
                del out[k]
        labels = out.keys()
        # labels = [ l.replace(' ', '\n') for l in labels ]
        pylab.figure(figsize=(12,12))
        pylab.pie(out.values(), labels=labels, labeldistance=1.3)
        pylab.savefig('dept_expenditure.png')

if __name__ == '__main__':
    retrieve()
    a = Analyzer()
    # a.crude_totals()
    a.dept_spend()

