import re
import urllib
from StringIO import StringIO

src_url = 'http://eh.net/databases/finance/Table%204.%20Govt%20revenue.txt'
extra_title = ' (for 17 Countries in the period 1880-1913)'
country_codes = {
        'AH' : 'Austro-Hungary',
        'ARGE' : 'Argentina',
        'BELG' : 'Belgium',
        'BRAZ' : 'Brazil',
        'DENM' : 'Denmark',
        'FRAN' : 'France',
        'GERM' : 'Germany',
        'GREE' : 'Greece',
        'ITAL' : 'Italy',
        'NETH' : 'Netherlands',
        'NORW' : 'Norway',
        'PORT' : 'Portugal',
        'RUSS' : 'Russian',
        'SPAI' : 'Spain',
        'SWED' : 'Sweden',
        'SWIT' : 'Switzerland',
        'UNIK' : 'United Kingdom',
        }

def download():
    fo = urllib.urlopen(src_url)
    stream = fo.read()
    fo.close()
    return StringIO(stream)

def tidy(fileobj):
    lines = fileobj.readlines()
    title = tidy_title(lines[0])
    data = format_data(lines[4:])
    header = format_header(lines[2])
    return title, header, data

def tidy_title(line):
    index = line.index('. ') + 2
    # :-1 to remove carriage return
    title = line[index:-1]
    title = title + extra_title
    return title

def format_data_line(line):
    spaces = '\s+'
    out = re.sub(spaces, ',', line)
    # strip trailing comma
    out = re.sub(',$', '', out)
    # strip leading comma
    out = re.sub('^,', '', out)
    # replace '.' by empty value
    out = out.replace(',.,', ',,')
    # change year: to year i.e. 1880: to 1880
    year_colon = '(\d{4}):'
    out = re.sub(year_colon, r'\1', out)
    return out

def format_header(line):
    header = format_data_line(line)
    items = header.split(',')
    newcols = []
    for item in items:
        newvalue = country_codes[item]
        newcols.append(newvalue)
    header = ','.join(newcols)
    header = 'Year,' + header
    return header

def format_data(data):
    out = []
    for line in data:
        out.append(format_data_line(line))
    out = '\n'.join(out)
    return out

# this will go in ini style file
# multiline strings must have indent on all lines after first (including blank
# ones)
source_info = \
'''
source: Original data retrieved from <http://eh.net/databases/finance/> and then
  reformatted (see ../prepare.py).
  
  That page also provides the following information about the
  origins of the data:
  
  > Below are data tables which accompany Marc Flandreau and Fredreric Zumer's book
  > The Making of Global Finance, 1880-1913, OECD 2004. Please refer to it when
  > quoting sources. A detailed presentation of the data and methodology is
  > available in the monograph which can be read online.
  >
  > The tables provide economic data for seventeen countries:
  >
  > Argentina, Austria-Hungary, Belgium, Brazil, Denmark, France, Germany,
  > Greece, Italy, Netherlands, Norway, Portugal, Russia, Spain, Sweden,
  > Switzerland, and the United Kingdom.
  >     
  > Except when stated otherwise, units are million of domestic currency. The
  > national units are: Argentina: paper peso; Austria-Hungary: florin;
  > Belgium: Belgian franc; Brazil: Brazilian milreis; Denmark: kroner; France:
  > French franc; Germany: mark; Greece: drachma, Italy: lira, Netherlands:
  > Dutch florin; Norway: kroner, Portugal: Portuguese milreis; Spain: peseta;
  > Sweden: kronor; Switzerland: Swiss franc; Russia: ruble; United Kingdom:
  > pound.
'''

class TestThis:
    ## TODO
    pass

if __name__ == '__main__':
    f1 = download()
    meta = file('metadata.txt', 'a')
    title, header, data = tidy(f1)
    meta.write('title = %s' % title)
    meta.write(source_info)
    meta.close()
    csvfo = file('data.csv', 'w')
    csv_content = header + '\n' + data
    csvfo.write(csv_content)
    csvfo.close()
    # print title, header
    # print data

