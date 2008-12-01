import urllib
urls = { 'ftp://ftp.bls.gov/pub/special.requests/lf/aat1.txt' : 'aat1.txt',
        # 'ftp://ftp.bls.gov/pub/special.requests/lf/aat2.txt' : 'aat2.txt'
        }

def get():
    for k,v in urls.items():
        urllib.urlretrieve(k,v)

import re
space = re.compile(r'\s\s+')
def get_row(line, minimum_number_of_columns=3):
    # need 2 or more spaces!
    row = space.split(line)
    if len(row) <= minimum_number_of_columns:
        return None
    # clean up first row (what do we do about footnotes)
    row[0] = row[0].replace('.', '')
    # extract fn
    # either yyyy (fn) or just yyyy
    out = row[0].split()
    if len(out) == 2:
        fn = out[1][1:-1]
    else:
        fn = ''
    row[0] = out[0]
    row.append(fn)
    row[1:-1] = [ xx.replace(',', '') for xx in row[1:-1] ]
    return row

# TODO
def get_headings(lines):
    rows = []
    for line in lines:
        rows.append(space.split(line))
    rows.reverse()
    out = rows[0]
    for row in rows[1:-1]:
        for ii in range(len(row)):
            out[ii] += row[ii]
    return out

def parse_file(fo, title_line, value_range, footnote_range=[]):
    count = 0
    title = ''
    # TODO: headings
    headings = []
    rows = []
    fns = []
    for line in fo:
        line = line.strip()
        # not the same line in every file!!
        if count == title_line:
            title = line
        if count in value_range:
            row = get_row(line)
            # remove blank lines
            if row:
                rows.append(row)
        if count in footnote_range:
            # More hacking because fns can spill over multiple lines
            # Assume never more than five fns
            # TODO make this more robust ...
            if line[0] in ['1', '2', '3', '4', '5' ]:
                fns.append(line)
            else:
                fns[-1] += ' ' + line
        count += 1
    return title, rows, fns

# TODO: col titles (a complete mess ...)
def parse_1(fo):
    comments = 'Persons 14 years of age and over 1940-1947, Persons 16 years of age and over 1948 onwards'
    return parse_file(fo, 5, range(22, 101), [102, 103])

def parse_2(fo):
    return parse_file(fo, 3, range(20, 103), [103])

def test_get_row():
    line = '2006 (1)......................  228,815    151,428      66.2 144,427 63.1        2,206     142,221      7,001       4.6      77,387'
    row = get_row(line)
    assert row[0] == '2006'
    assert row[-1] == '1'
    assert row[1] == '228815'

def test_headings():
    teststr = \
'''                    Civilian                                           Employed                         Unemployed        Not in  
                  Year               noninsti-                                                                                              labor  
                                     tutional               Percent                                                                         force  
                                    population    Total       of                  Percent                Nonagri-               Percent            
                                                          population    Total       of         Agri-     cultural    Number       of               
                                                                                population    culture   industries               labor             
                                                                                                                                 force            ''' 
    # TODO
    # out = get_headings(teststr.splitlines())
    # assert out[0] == 'Year'


def test_parse_1():
    fo = file('aat1.txt')
    title, rows, fns = parse_1(fo)
    assert title == '1.  Employment status of the civilian noninstitutional population, 1940 to date'
    assert rows[0][0].startswith('1940')
    assert rows[-1][0].startswith('2006')
    assert len(rows) == 2007-1939
    assert len(fns) == 1
    assert fns[0].startswith('1 Not strictly')
    assert fns[0].endswith('Estimates of Error.')

def test_parse_2():
    fo = file('aat2.txt')
    title, rows, fns = parse_2(fo)
    assert title == '2.  Employment status of the civilian noninstitutional population 16 years and over by sex, 1971 to date' 
    assert len(rows) == 2 * (2006-1971) + 2
    assert rows[0][0].startswith('1971')
    assert rows[-1][0].startswith('2006')

import csv
def make_csv():
    for fn in urls.values():
        fo = file(fn)
        title, rows, fns = parse_1(fo)
        csvfn = fn[:-3] + 'csv'
        csvfo = file(csvfn , 'w')
        writer = csv.writer(csvfo)
        for row in rows:
            writer.writerow(row)
        csvfo.close()
        print 'CSV file %s written ok' % csvfn
        print 'Title: ', title
        print 'Footnotes: ', fns

import os
def execute():
    get()
    make_csv()
    os.symlink('aat1.csv', 'data.csv')

if __name__ == '__main__':
    execute()

    # fn = 'aat1.txt'
    # fo = file(fn)
    # title, rows, fns = parse_1(fo)
    # print title, fns, rows
