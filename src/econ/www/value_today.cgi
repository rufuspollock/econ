#!/usr/bin/env python

import sys
import cgi
import cgitb; cgitb.enable()

def renderPage():
    print 'Content-type: text/html\n\n'
    form = cgi.FieldStorage()
    year = 2001
    if form.has_key('year'):
        year = form['year'].value
    errorMessage = ''
    value2002 = 0
    try:
        value2002 = getCurrentValue(float(year), 2002)
    except Exception, inst:
        errorMessage = '<p><strong>There was an error: ' +  str(inst) + '</strong></p>'
    template = """
<html>
    <head>
    </head>
    <body>
        %(error_message)s
        <form action="value_today.cgi" method="GET">
            Year: <input name="year" value="%(year)s" />
            <br />
            <input type="submit" value="Get Current Value" />
        </form>
        <p>
            Value of one pound from %(year)s in 2002 was: %(value_2002)s
        </p>
    </body>
</html>""" % { 'error_message': errorMessage, 'year' : year, 'value_2002' : value2002 }
    print template
    

def getCurrentValue(startYear, endYear):
    import econ.data
    import econ.store
    import econ.DiscountRate
    databundle = econ.store.index['uk_price_index_1850-2002_annual']
    filePath = databundle.data_path
    ts1 = econ.data.getTimeSeriesFromCsv(file(filePath))
    discounter = econ.DiscountRate.DiscountRateHistorical(ts1)
    return discounter.getReturn(startYear, endYear)


if __name__ == '__main__':
    renderPage()
