import os
import urllib

import econ.data.tabular
import econ.data.misc
import econ.data.swiss as tl

base_page = 'http://www.ers.usda.gov/Data/Wheat/'
data_index = 'http://www.ers.usda.gov/Data/Wheat/WheatYearbook.aspx'

recent_data_url = 'http://www.ers.usda.gov/data/wheat/yearbook/WheatYearbookTables-Recent.xls'
all_data_url = 'http://www.ers.usda.gov/data/wheat/yearbook/WheatYearbookTables-Full.xls'
all_fn = 'data_original.xls'

VERBOSE = True

def download():
    if VERBOSE:
        print 'Starting download.'
        print 'Please be patient: the file is large so this may take some time.'
    urllib.urlretrieve(all_data_url, all_fn)

def info():
    print tl.xls_info(all_fn)
    print tl.xls_sheet_info(all_fn, 0)
    # print tl.xls_sheet_info(all_fn, 1)

def get_table_index():
    reader = econ.data.tabular.XlsReader()
    tabdata = reader.read(file(all_fn))
    data = [ row[0] for row in tabdata.data ]
    table_names = filter(lambda x: x.startswith('Table '), data)
    return table_names

class SheetParser(object):
    def get_sheet(self, index):
        reader = econ.data.tabular.XlsReader()
        tabdata = reader.read(file(all_fn), index)
        return tabdata.data

    def format_line(self, line):
        year = line[0]
        year = year.split('/')[0]
        year = int(year)
        def clean(value):
            if value == '--':
                return ''
            else:
                return econ.data.misc.floatify(value)
        out = [year] + [ clean(value) for value in line[1:] ]
        return out

    def extract_table_1(self):
        data = self.get_sheet(1)
        headings = ['Market Year', 'Planted acreage (millions)',
            'Harvested acreage (millions)', 'Production (millions of bushels)',
            'Yield (bushels per acre)', 'Weighted-average farm price ($ per bushel)'
            ]
        # remove headings and footnotes
        data = data[3:-3]
        # break into sections based on blank lines
        is_blank = lambda x: data[x][1] == ''
        blank_rows = filter(is_blank, range(len(data)))
        # put in start item
        blank_rows = [-1] + blank_rows
        sections = [ data[blank_rows[ii]+1:blank_rows[ii+1]] for ii in
                range(len(blank_rows) - 1) ]
        results = {}
        def parse_section(section):
            out = [ self.format_line(row[1:]) for row in section ]
            return out

        for section in sections:
            results[section[0][0]] = econ.data.tabular.TabularData(
                    data=parse_section(section),
                    header=headings)
        return results

def test_get_table_index():
    tns = get_table_index()
    assert tns[0] == u'Table 1--Wheat: Planted acreage, harvested acreage, production, yield, and farm price'

def test_extract_table_1():
    parser = SheetParser()
    out = parser.extract_table_1()
    assert len(out) == 6
    all = out['All wheat'].data
    print all[0]
    assert all[0][0] == 1866
    assert all[1][1] == ''
    assert all[2][2] == 19.140
    assert all[79][4] == 1060.0



def main():
    if not os.path.exists(all_fn):
        download()
    index = get_table_index()
    # sheet 1 is special since it contains multiple items
    parser = SheetParser()
    tables = parser.extract_table_1()
    writer = econ.data.tabular.CsvWriter()
    table_list = []
    for name in tables:
        fn = 'table_1_%s.csv' % name.lower().replace(' ', '_')
        writer.write(file(fn, 'wb'), tables[name])
        title = index[0] + ' (%s)' % name
        table_list.append((fn, title))
    # finally copy one table to default position
    default = file('table_1_all_wheat.csv')
    file('data.csv', 'w').write(default.read())
    for table in table_list:
        print '[%s]' % table[0]
        print 'title: %s' % table[1]
        print


if __name__ == '__main__':
    main()
    # info()
