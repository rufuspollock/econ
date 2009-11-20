url = 'http://www.econ.yale.edu/~shiller/data/ie_data.xls'
cache = 'cache'

import swiss
import swiss.tabular
cache = swiss.Cache(cache)

class Extractor(object):
    def execute(self):
        fp = cache.retrieve(url)
        reader = swiss.tabular.XlsReader(fp)
        # print reader.info()
        tabdata = reader.read()
        # clean up data
        data = tabdata.data
        # headings spread across rows 5-8
        headings = zip(*data[4:8])
        tabdata.header = [ ' '.join(cols).strip() for cols in headings ]
        data = tabdata.data[8:-1]
        transposed = zip(*data)
        # get rid of odd date e.g. 1871.01 and replace with date fraction
        fraction = transposed[5]
        del transposed[5]
        del transposed[-1]
        transposed[0] = fraction
        tabdata.data = zip(*transposed)
        del tabdata.header[5]
        del tabdata.header[-1]
        writer = swiss.tabular.CsvWriter()
        writer.write(tabdata, open('data.csv', 'w'))


if __name__ == '__main__':
    Extractor().execute()

