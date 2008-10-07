import os
import urllib
import econ.data.tabular as T
import pylab

# download by hand gives ...
downloaded = 'bbk_WU5500.csv'

def download():
    # does not work as goes via php ...
    url = 'http://www.bundesbank.de/statistik/statistik_zeitreihen_download.en.php?func=directcsv&from=&until=&filename=bbk_WU5500&csvformat=en&euro=mixed&tr=WU5500'
    urllib.urlretrieve(url, downloaded)

# TODO: clean up?

def plot():
    fn = 'data.csv' 
    r = T.CsvReader()
    tdata = r.read(file(fn))
    data = tdata.data[5:-2]
    data = zip(*data)
    dates = data[0]
    values = data[1]
    def cvt(indate):
        year, month = indate.split('-')
        return float(year) + float(month)/12.0
    dates = [ cvt(d) for d in dates ] 
    values = [ float(v) for v in values ]
    pylab.plot(dates, values)
    pylab.savefig('gold_prices.png')

if __name__ == '__main__':
    plot()
