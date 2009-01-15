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
    doc = open(retriever.retrieve(url).read())
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
    sj.dump(xls_urls, open(infopath, 'w'), indent=4)

import econ.data.tabular as T
class Analyzer():
    def __init__(self):
        self.xls_urls = sj.load(open(infopath))

    def extract_simple(self):
        # fp = retriever.filepath(self.xls_urls[2])
        fp = retriever.filepath('pesa0809chapter1.xls')
        print fp
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
        # fp = retriever.filepath(self.xls_urls[6])
        fp = retriever.filepath('pesa_2008_chapter5_tables.xls')
        print fp
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

if __name__ == '__main__':
    retrieve()
    a = Analyzer()
    print a.extract_simple()[0].keys()
    print a.extract_dept_spend()

