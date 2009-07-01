import os
import re
import urllib
import logging
import simplejson

logger = logging.getLogger('econdata.ukgovfinances')
logging.basicConfig()
logger.setLevel(logging.INFO)

import BeautifulSoup as bs

from swiss.cache import Cache
import swiss as swiss

cache = os.path.join(os.path.dirname(__file__), 'cache')
baseurl = 'http://www.hm-treasury.gov.uk'
url = 'http://www.hm-treasury.gov.uk/pespub_pesa08.htm'
retriever = Cache(cache)
infopath = os.path.join(cache, 'info.js')

dbpath = os.path.join(cache, 'ukgovfinances.db')

def retrieve():
    xls_urls = []
    doc = open(retriever.retrieve(url)).read()
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
    simplejson.dump({'urls': xls_urls}, open(infopath, 'w'), indent=4)


import swiss.tabular as T
class Analyzer():
    def __init__(self):
        self.info = simplejson.load(open(infopath)) 
        self.xls_urls = self.info['urls']

    def summary(self, force=False):
        if 'summary' in self.info and not force:
            return self.info['summary']
        else:
            return self._extract_summary()

    def _extract_summary(self):
        results = {}
        for url in self.xls_urls:
            logger.info(url)
            fp = retriever.filepath(url)
            r = T.XlsReader(open(fp))
            td = r.read()
            # 4th line has title
            set_title = td.data[3][0]
            # Great! sometimes in row 1 sometimes in row 2
            def gettitle(row):
                if len(row) >= 2 and row[1]: return row[1]
                else: return row[0]
            table_titles = [ gettitle(row) for row in td.data[4:] if row[0] ]
            results[url] = { 'title': set_title,
                'tables': table_titles
                }
        self.info['summary'] = results
        simplejson.dump(self.info, open(infopath, 'w'), indent=4)
        return results

    def dump_summary_to_csv(self):
        '''Dump table summary as csv'''
        import csv
        path = retriever.filepath('table_summary.csv')
        fo = open(path, 'w')
        writer = csv.writer(fo)
        writer.writerow(['Url/Chapter', 'Table', 'Comments'])
        for url in self.xls_urls:
            info = self.info['summary'][url]
            writer.writerow([])
            writer.writerow([url])
            writer.writerow([info['title']])
            writer.writerow([])
            for table in info['tables']:
                writer.writerow(['', table])
        fo.close()

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

    def _process_sheet(self, tabular_data):
        import db
        repo = db.Repository('sqlite:///%s' % dbpath)
        years = range(2002, 2011)
        td = tabular_data
        cells = td.data
        title = cells[0][0]
        table = db.PesaTable(title=title)
        footnotes = []
        for lastrow in reversed(cells):
            if len(lastrow) > 2: # into the data
                break
            foot = lastrow[0].strip()
            if foot:
                footnotes.append(foot)
        table.footnotes = simplejson.dumps(footnotes)
        entries = {}
        for row in cells[6:]:
            if row[1]: # not a subheading or footnote
                series_name = row[0]
                for (year, cell) in zip(years, row[1:10]):
                    db.Expenditure(
                            title=series_name,
                            date=unicode(year),
                            amount=swiss.floatify(cell),
                            pesatable=table,
                            )
        db.Session.flush()

    def load_all(self):
        for ii in range(1,5):
            fp = retriever.filepath('pesa0809chapter%s.xls' % ii)
            logger.info('Processing file: %s' % fp)
            r = T.XlsReader()
            r.read(open(fp), 0)
            num_sheets = r.book.nsheets
            for sheet_index in range(1, num_sheets):
                logger.info('Processing sheet: %s' % sheet_index)
                td = r.read(open(fp), sheet_index)
                self._process_sheet(td)

    def pesa_chapter_1(self):
        fp = retriever.filepath('pesa0809chapter1.xls')
        r = T.XlsReader()
        for sheet_index in range(1,16):
            logger.info('Processing sheet: %s' % sheet_index)
            td = r.read(open(fp), sheet_index)
            self._process_sheet(td)

    def pesa_chapter_2(self):
        fp = retriever.filepath('pesa0809chapter2.xls')
        logger.info('Processing file: %s' % fp)
        r = T.XlsReader()
        for sheet_index in range(1,5):
            logger.info('Processing sheet: %s' % sheet_index)
            td = r.read(open(fp), sheet_index)
            self._process_sheet(td)
    
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
    
    def extract_dept_spend_for_jit(self):
        spend = self.extract_dept_spend()
        import uuid
        def makenode(name, value):
            return {'children': [], 'id': str(uuid.uuid4()), 'name': name,
                    'data': {
                        '$area': value,
                        }
                    }
        total = sum([ x for x in spend.values() ])
        children = [ makenode(k,v) for (k,v) in spend.items() ]
        jitjs = makenode('root', total)
        jitjs['children'] = children
        import simplejson
        return simplejson.dumps(jitjs, indent=2)

import optparse
if __name__ == '__main__':
    usage = '''%prog <action>

retrieve: retrieve files to local cache.
summary: summary of PESA tables
load
db clean
demo
dept: dept spend
'''
    parser = optparse.OptionParser(usage) 
    options, args = parser.parse_args()
    action = args[0]
    a = Analyzer()
    if action == 'retrieve':
        retrieve()
    elif action == 'summary':
        out = a.summary()
        print 'Dumping to csv ...'
        a.dump_summary_to_csv()
        import pprint
        pprint.pprint(out)
    elif action == 'db':
        action2 = args[1]
        if action2 == 'clean':
            if os.path.exists(dbpath):
                os.remove(dbpath)
    elif action == 'load':
        a.load_all()
        # a.pesa_chapter_1()
        # a.pesa_chapter_2()
    elif action == 'demo':
        print a.extract_simple()[0].keys()
        # print a.extract_dept_spend()
    elif action == 'dept':
        spend = a.extract_dept_spend_for_jit()
        print spend
    else:
        parser.print_help()

