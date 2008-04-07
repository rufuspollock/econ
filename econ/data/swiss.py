'''A "swiss army" knife toolset for downloading, extracting and investigating
data.
'''

import pprint
def xls_info(fn):
    '''Get some info about an xls file.'''
    import xlrd
    book = xlrd.open_workbook(fn)
    info = ''
    info += 'The number of worksheets is: %s\n' % book.nsheets
    info += 'Worksheet name(s):\n' % book.sheet_names()
    count = -1
    for sn in book.sheet_names():
        count += 1
        info += '%s  %s\n' % (count, sn)
    # booksheet = book.sheet_by_index(sheet_index)
    return info

def xls_sheet_info(fn, sheet_index):
    '''Get some info about an xls sheet.'''
    import xlrd
    book = xlrd.open_workbook(fn)
    sh = book.sheet_by_index(sheet_index)
    info = sh.name + '\n'
    info += 'Rows: %s Cols: %s\n\n' % (sh.nrows, sh.ncols)
    MAX_ROWS = 30
    for rx in range(min(sh.nrows, MAX_ROWS)):
        info += str(sh.row(rx)) + '\n'
    return info
