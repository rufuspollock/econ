# Extract all datasets listed on <http://eh.net/databases/finance/> and convert
# to standard data bundles
import re
import urllib
from StringIO import StringIO

base_url = 'http://eh.net/databases/finance/'
extra_title = ' (for 17 Countries in the period 1880-1913)'
# this will go in ini style file
# multiline strings must have indent on all lines after first (including blank
# ones)
source_info = \
'''source: Original data retrieved from %s and then reformatted (see
  ../prepare.py).
  
  Home page for the data is <http://eh.net/databases/finance/> which contains
  the following information about the origins of the data:
  
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
  > pound.'''

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

def download(url):
    fo = urllib.urlopen(url)
    stream = fo.read()
    fo.close()
    return StringIO(stream)

def tidy(fileobj):
    lines = fileobj.readlines()
    title = tidy_title(lines[0])
    # header either start on 3rd or 4th lines depending on notes and blanks
    # always have a single space until data 
    if lines[2].strip():
        header = lines[2]
        data = lines[4:]
    else:
        header = lines[3]
        data = lines[5:]
    header = format_header(header)
    data = format_data(data)
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

def get_file_urls():
    import twill.commands as w
    w.go(base_url)
    urls = []
    for link in w.showlinks():
        url = link.url
        if url.startswith('Table') and url.endswith('.txt'):
            urls.append(url)
    return urls

def create_bundle(url, title, header, data):
    # 'http://eh.net/databases/finance/Table%201.%20Interest%20Service.txt'
    dataset_number = url[39:41]
    import econ.store.bundle
    import uuid
    id = uuid.uuid4()
    dest_path = os.path.abspath('./tmp')
    path = os.path.join(dest_path, dataset_number)
    bndl = econ.store.bundle.DataBundle(id=id, path=path)
    bndl.metadata['title'] = title
    source = source_info % url
    bndl.metadata['source'] = source
    csv_content = header + '\n' + data
    fo = file(bndl.data_path)
    fo.write(csv_content)

#    meta = file('metadata.txt', 'a')
#    meta.write('title = %s' % title)
#    meta.write(source_info)
#    meta.close()
#    csvfo = file('data.csv', 'w')
#    csv_content = header + '\n' + data
#    csvfo.write(csv_content)
#    csvfo.close()

def process_all():
    urls = get_file_urls()
    print urls
    return
    for url in urls:
        f1 = download(url)
        title, header, data = tidy(f1)
        create_bundle(url, title, data)

class TestThis:

    def test_get_file_urls(self):
        out = get_file_urls()
        assert len(out) == 21
        assert out[0].endswith('.txt')
        assert out[-1].endswith('.txt')

if __name__ == '__main__':
    # src_url = 'http://eh.net/databases/finance/Table%204.%20Govt%20revenue.txt'
    # src_url = 'http://eh.net/databases/finance/Table%201.%20Interest%20Service.txt'
    # f1 = download(src_url)
    # title, header, data = tidy(f1)
    # print title, header
    # print data
    process_all()

