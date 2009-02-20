import os
import re
import urllib

import simplejson as sj

import econ.data
# import BeautifulSoup as bs
from econ.data import Retriever

cache = os.path.join(os.path.dirname(__file__), 'cache')
retriever = Retriever(cache)

url = 'http://www.littletechshoppe.com/ns1625/winchest.html'

localfp = retriever.retrieve(url)
# soup = bs.BeautifulSoup(open(localfp).read())

def get_tables():
    reader = econ.data.HtmlReader()
    reader.read(open(localfp))
    tables = reader.tables
    wanted = tables[:4] + tables[5:7] + tables[8:10]
    out = econ.data.TabularData()
    out.header = wanted[0][0]
    for t in wanted:
        out.data += t
    writer = econ.data.CsvWriter()
    writer.write(open('data.csv', 'w'), out)

get_tables()
