import os
import re
import urllib

from econ.data import Retriever

import BeautifulSoup as bs

cache = os.path.abspath('./cache')
url = 'http://www.hm-treasury.gov.uk/economic_data_and_tools/finance_spending_statistics/pes_publications/pespub_pesa07.cfm'
retriever = Retriever(cache)
doc = retriever.retrieve(url).read()

soup = bs.BeautifulSoup(doc)
# find all csv
for href in soup.findAll('a', href=re.compile('.*\.csv')):
    print href

# find all xls
for href in soup.findAll('a', href=re.compile('.*\.xls')):
    print href
